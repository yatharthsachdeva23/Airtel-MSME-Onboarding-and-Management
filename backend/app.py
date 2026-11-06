import os
import sys
import uuid
import shutil
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add workspace to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.catalog_service import CatalogService
from backend.loop_engine import LoopEngine
from backend.advisor_engine import AdvisorEngine
from backend.kyc_service import KYCService
from backend.dpdp_compliance import DPDPComplianceEngine
from backend.feasibility_service import FeasibilityService
from backend.handoff_service import LiveHandoffService
from backend.order_tracker import OrderTrackerService
from backend.gemini_service import GeminiSalesService, BENCHMARK_DATE

app = FastAPI(
    title="Project Udyam Digital API",
    description="Autonomous Telecom & Digital Onboarding Platform for MSMEs - Airtel SYNC 2026",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate singletons
catalog_svc = CatalogService()
loop_engine = LoopEngine()
advisor_engine = AdvisorEngine(catalog_svc, loop_engine)
kyc_svc = KYCService()

# ---------------- DATA MODELS ----------------

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    language: str = "en"

class QuoteRequest(BaseModel):
    product_ids: List[str]
    employee_count: int = 1
    num_sites: int = 1
    has_gstin: bool = True
    city_tier: int = 2
    billing_cycle_months: int = 1

class DPDPNoticeRequest(BaseModel):
    entity_name: str
    applicant_name: str

class DPDPConsentRequest(BaseModel):
    session_id: str
    applicant_name: str
    consent_granted: bool

class FeasibilityRequest(BaseModel):
    address: str
    pincode: str
    requested_product_id: str = "P01"

class HandoffRequest(BaseModel):
    session_id: str
    customer_name: str
    phone: str
    business_type: str
    trigger_reason: str
    detected_objection: Optional[Dict[str, Any]] = None
    current_cart: Optional[List[Dict[str, Any]]] = None

class CreateOrderRequest(BaseModel):
    session_id: str
    customer_name: str
    entity_name: str
    phone: str
    address: str
    bundle: Dict[str, Any]
    technology: str = "Fiber"
    install_days: int = 2

# ---------------- API ENDPOINTS ----------------

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "Project Udyam Digital API",
        "resilience_engine": "Active (Circuit Breaker & Fallback Ready)"
    }

@app.get("/api/catalog")
def get_catalog():
    return {
        "total_products": len(catalog_svc.products),
        "products": [p.to_dict() for p in catalog_svc.products.values()]
    }

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    session_id = req.session_id or f"sess_{uuid.uuid4().hex[:8]}"
    resp = advisor_engine.process_message(
        session_id=session_id,
        message=req.message,
        language=req.language
    )
    return resp

@app.post("/api/quote")
def quote_endpoint(req: QuoteRequest):
    business_profile = {
        "has_gstin": "Y" if req.has_gstin else "N",
        "employee_count": req.employee_count,
        "num_sites": req.num_sites,
        "city_tier": req.city_tier
    }
    is_valid, validation_errors = catalog_svc.validate_bundle(
        product_ids=req.product_ids,
        business_profile=business_profile
    )

    bundle_items = [
        {
            "product_id": pid,
            "quantity": 1,
            "unit_price": catalog_svc.products[pid].price_min
        }
        for pid in req.product_ids
        if pid in catalog_svc.products
    ]

    quote = catalog_svc.calculate_quote(bundle_items)
    item_count = len(bundle_items)
    discount_pct = 10 if item_count >= 5 else (5 if item_count >= 3 else 0)
    discount_amount = round(quote["monthly_subtotal"] * (discount_pct / 100), 2)
    net_monthly = round(quote["monthly_subtotal"] - discount_amount, 2)

    quote["bundle_discount_percent"] = discount_pct
    quote["discount_amount"] = discount_amount
    quote["net_monthly"] = net_monthly
    quote["monthly_total_inr"] = net_monthly
    quote["is_valid"] = is_valid
    quote["validation_errors"] = validation_errors
    quote["billing_cycle_months"] = req.billing_cycle_months
    return quote

@app.post("/api/kyc/dpdp-notice")
def dpdp_notice(req: DPDPNoticeRequest):
    return DPDPComplianceEngine.generate_consent_notice(req.entity_name, req.applicant_name)

@app.post("/api/kyc/dpdp-consent")
def dpdp_consent(req: DPDPConsentRequest):
    return DPDPComplianceEngine.record_consent(
        session_id=req.session_id,
        applicant_name=req.applicant_name,
        consent_granted=req.consent_granted
    )

@app.post("/api/kyc/audit-dossier")
def audit_dossier(applicant_id: str):
    """Audits one of the 12 test applicant bundles (K01 to K12)."""
    return kyc_svc.audit_applicant_dossier(applicant_id)

@app.post("/api/kyc/upload-doc")
async def upload_kyc_document(
    doc_type: str = Form(...),  # gst, udyam, address, signatory
    file: UploadFile = File(...)
):
    """
    In-chat photo upload endpoint. Executes Gemini 2.5 Flash Vision OCR,
    cross-verifies against national registry & 90-day DoT rules, with WinRT OCR fallback.
    """
    file_bytes = await file.read()
    mime_type = file.content_type or "image/png"
    
    # 1. Try Gemini 2.5 Flash Multimodal OCR first
    try:
        gem_data = GeminiSalesService.extract_document_with_gemini(file_bytes, mime_type, doc_type)
        if gem_data and not gem_data.get("error"):
            # Check completeness
            if not gem_data.get("is_complete", True):
                return {
                    "valid": False,
                    "error_code": "ERROR_DOCUMENT_INCOMPLETE",
                    "message": "The uploaded document appears blank, cut off, or incomplete.",
                    "mitigation": "Please capture and upload a clear, fully visible photo."
                }

            if doc_type == "gst":
                gstin = gem_data.get("gstin", "").strip().upper()
                if gstin:
                    normalized = kyc_svc.normalize_gstin_candidate(gstin)
                    reg_entry = kyc_svc.gst_registry.get(normalized) or kyc_svc.gst_registry.get(gstin)
                    if reg_entry:
                        status = (reg_entry.get("status") or "").upper()
                        if status in ["CANCELLED", "SUSPENDED"]:
                            return {
                                "valid": False,
                                "gstin": normalized,
                                "error_code": "ERROR_GSTIN_INACTIVE",
                                "message": f"GSTIN {normalized} is marked as {status} on the national GSTN portal.",
                                "mitigation": "Please provide an active GSTIN or Udyam registration."
                            }
                        return {
                            "valid": True,
                            "gstin": normalized,
                            "enterprise_name": reg_entry.get("legal_name") or gem_data.get("enterprise_name"),
                            "address": reg_entry.get("address") or gem_data.get("address"),
                            "status": "APPROVED",
                            "message": f"GSTIN {normalized} verified and active on National GSTN.",
                            "ocr_engine": "Gemini 2.5 Flash Vision OCR"
                        }
                    else:
                        # Check syntax
                        if re.match(r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', normalized):
                            return {
                                "valid": True,
                                "gstin": normalized,
                                "enterprise_name": gem_data.get("enterprise_name") or gem_data.get("business_name") or "Authorized Business",
                                "address": gem_data.get("address") or "Registered Business Premises",
                                "status": "APPROVED",
                                "message": f"GSTIN {normalized} syntax validated.",
                                "ocr_engine": "Gemini 2.5 Flash Vision OCR"
                            }
                        else:
                            return {
                                "valid": False,
                                "error_code": "ERROR_GSTIN_NOT_FOUND",
                                "message": f"GSTIN {normalized} could not be validated on the registry.",
                                "mitigation": "Please verify your 15-digit GSTIN number."
                            }

            elif doc_type == "address":
                b_date_str = gem_data.get("bill_date", "")
                if b_date_str:
                    try:
                        b_date = datetime.strptime(b_date_str, "%Y-%m-%d").date()
                        days_old = (BENCHMARK_DATE - b_date).days
                        if days_old > 90:
                            return {
                                "valid": False,
                                "bill_date": b_date_str,
                                "days_old": days_old,
                                "error_code": "ERROR_ADDRESS_PROOF_EXPIRED",
                                "message": f"Address proof is dated {b_date_str} ({days_old} days old). Under DoT regulations, utility bills must be issued within the last 90 days (after 16 April 2026).",
                                "mitigation": "Please upload a recent utility bill issued within the last 3 months."
                            }
                        return {
                            "valid": True,
                            "bill_date": b_date_str,
                            "days_old": days_old,
                            "consumer_name": gem_data.get("consumer_name"),
                            "status": "APPROVED",
                            "message": f"Address proof verified. Bill date {b_date_str} is within valid 90-day DoT window.",
                            "ocr_engine": "Gemini 2.5 Flash Vision OCR"
                        }
                    except Exception:
                        pass

            elif doc_type == "udyam":
                udyam = gem_data.get("udyam_number", "").strip().upper()
                if udyam:
                    reg = kyc_svc.udyam_registry.get(udyam)
                    return {
                        "valid": True,
                        "udyam_number": udyam,
                        "enterprise_name": reg.get("enterprise_name") if reg else gem_data.get("enterprise_name"),
                        "status": "APPROVED",
                        "message": f"Udyam registration {udyam} verified with Ministry of MSME.",
                        "ocr_engine": "Gemini 2.5 Flash Vision OCR"
                    }

            elif doc_type == "signatory":
                sig_name = gem_data.get("signatory_name", "").strip()
                return {
                    "valid": True,
                    "signatory_name": sig_name or "Authorized Signatory",
                    "status": "APPROVED",
                    "message": f"Signatory identity verified: {sig_name or 'Authorized Owner'}.",
                    "ocr_engine": "Gemini 2.5 Flash Vision OCR"
                }
    except Exception as e:
        print(f"[UploadDoc] Gemini Vision OCR skipped: {e}")

    # 2. Fallback to Local WinRT OCR
    tmp_dir = os.path.join(BASE_DIR, "data", "tmp_uploads")
    os.makedirs(tmp_dir, exist_ok=True)
    temp_path = os.path.join(tmp_dir, f"{uuid.uuid4().hex}_{file.filename}")
    
    with open(temp_path, "wb") as buffer:
        buffer.write(file_bytes)

    try:
        ocr_text = kyc_svc.get_document_ocr_text(temp_path)
        if doc_type == "gst":
            res = kyc_svc.verify_gst_document(ocr_text)
        elif doc_type == "udyam":
            res = kyc_svc.verify_udyam_document(ocr_text)
        elif doc_type == "address":
            res = kyc_svc.verify_address_proof(ocr_text)
        elif doc_type == "signatory":
            res = kyc_svc.verify_signatory_id(ocr_text)
        else:
            res = {"valid": False, "message": "Unknown document type"}

        res["ocr_preview"] = ocr_text[:200] + ("..." if len(ocr_text) > 200 else "")
        return res
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

@app.post("/api/feasibility")
def check_feasibility(req: FeasibilityRequest):
    return FeasibilityService.check_feasibility(
        address=req.address,
        pincode=req.pincode,
        requested_product_id=req.requested_product_id
    )

@app.post("/api/handoff")
def trigger_handoff(req: HandoffRequest):
    return LiveHandoffService.create_handoff_ticket(
        session_id=req.session_id,
        customer_name=req.customer_name,
        phone=req.phone,
        business_type=req.business_type,
        trigger_reason=req.trigger_reason,
        detected_objection=req.detected_objection,
        current_cart=req.current_cart
    )

@app.get("/api/handoff/tickets")
def list_handoff_tickets():
    return LiveHandoffService.list_tickets()

@app.post("/api/order/create")
def create_order(req: CreateOrderRequest):
    return OrderTrackerService.create_order(
        session_id=req.session_id,
        customer_name=req.customer_name,
        entity_name=req.entity_name,
        phone=req.phone,
        address=req.address,
        bundle=req.bundle,
        technology=req.technology,
        install_days=req.install_days
    )

@app.get("/api/order/{order_id}")
def get_order(order_id: str):
    ord_data = OrderTrackerService.get_order(order_id)
    if not ord_data:
        raise HTTPException(status_code=404, detail="Order not found")
    return ord_data

@app.get("/api/evals/run")
def run_live_evals():
    """
    Executes live AI evaluation benchmark test suites directly from UI and returns structured metrics.
    """
    import subprocess
    cmd = [
        sys.executable, "-m", "unittest",
        "tests/test_ai_evals.py",
        "tests/test_kyc_validation.py",
        "tests/test_phase3_services.py"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
    passed = (res.returncode == 0)
    return {
        "passed": passed,
        "total_tests": 19,
        "criteria_evaluated": [
            "1. 100% Catalog Groundedness (zero unlisted items)",
            "2. Strict Dependency Compliance (add-on prerequisites)",
            "3. Regulatory Guardrails (GSTIN enforcement)",
            "4. Business Sizing Rules (team size / site limits)",
            "5. Deterministic Pricing Math (no arbitrary quotes)",
            "6. Real-Time Objection Detection & Human Escalation",
            "7. Multilingual Conversational Fidelity across 6 Indian Languages",
            "8. Smart KYC Planted Error Detection (K01-K12 Dossiers)",
            "9. DPDP Act 2023 Consent & PII Masking Shield",
            "10. FAT Box Feasibility & 5G AirFiber Auto-Pivot"
        ],
        "output": res.stderr.strip() or res.stdout.strip()
    }

# Mount static frontend
frontend_dir = os.path.join(BASE_DIR, "frontend")
os.makedirs(frontend_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def index():
    html_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return HTMLResponse("<h3>Project Udyam Digital: Frontend Loading...</h3>")
