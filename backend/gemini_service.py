import os
import re
import json
import time
import base64
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, date

BENCHMARK_DATE = date(2026, 7, 15)

def get_gemini_api_key() -> str:
    """Retrieves GEMINI_API_KEY from environment or .env file."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return ""

CATALOG_CONTEXT = """
OFFICIAL ACCEL BUSINESS MSME PRODUCT CATALOG (25 PRODUCTS):

1. CONNECTIVITY:
- P01: Biz Fibre 100 — ₹999/mo | Setup: ₹0 | SLA: 5 days | Target: Micro retail, small office | 100 Mbps symmetric broadband, unlimited data, dual-band Wi-Fi router.
- P02: Biz Fibre 300 — ₹1,499/mo | Setup: ₹0 | SLA: 5 days | Target: Professional office, clinics, retail chains | 300 Mbps high-speed, free router, static IP optional.
- P03: Biz Fibre 1G — ₹3,999/mo | Setup: ₹0 | SLA: 7 days | Target: Multi-site, tech startups | 1 Gbps ultra-fast fiber, priority business peering. Requires GSTIN.
- P04: Biz 5G AirFiber 100 — ₹899/mo | Setup: ₹0 | SLA: 2 days | Target: Micro retail & sites without fiber | Wireless (5G FWA) plug-and-play broadband router.
- P05: Internet Leased Line 20 — ₹8,000/mo | Setup: ₹10,000 | SLA: 21 days | Target: Manufacturing, banks | Dedicated 1:1 unshared bandwidth, 99.5% uptime SLA. Requires GSTIN, min 10 employees.
- P06: Internet Leased Line 100 — ₹25,000/mo | Setup: ₹15,000 | SLA: 30 days | Target: Factories, IT hubs | 100 Mbps 1:1 symmetric leased line, 99.9% SLA. Requires GSTIN, min 25 employees.
- P07: Business Postpaid 299 — ₹299/mo per line | Setup: ₹0 | SLA: 1 day | 50 GB pooled data, unlimited voice calls.
- P08: Business Postpaid 599 — ₹599/mo per line | Setup: ₹0 | SLA: 1 day | 150 GB pooled data, roaming, priority care.
- P09: Backup 4G/5G Failover — ₹499/mo | Setup: ₹1,500 | SLA: 3 days | Automatic wireless failover router so UPI billing never drops when outdoor fiber cables are cut. Prereq: P01/P02/P03/P05/P06.
- P10: Managed SD-WAN — ₹2,500/mo per site | Setup: ₹5,000 | SLA: 14 days | Multi-site central link management, app-priority routing. Requires GSTIN, min 10 employees, min 3 sites.
- P11: Static IP — ₹200/mo per IP | Setup: ₹0 | SLA: 1 day | Fixed public IP for CCTV, remote access.

2. COMMUNICATION & VOICE:
- P12: Cloud Telephony / SIP — ₹1,000/mo | Setup: ₹2,000 | SLA: 5 days | Business phone lines over internet with IVR, call recording. Requires GSTIN, min 3 employees.
- P13: Toll-free Number — ₹1,500/mo | Setup: ₹1,000 | SLA: 3 days | National 1800 number routed to mobile/telephony. Requires GSTIN.
- P14: Business SMS 10k — ₹1,500/mo | Setup: ₹0 | SLA: 4 days | 10,000 promotional & transactional SMS/mo. Requires GSTIN.
- P15: WhatsApp Business API Starter — ₹999/mo | Setup: ₹0 | SLA: 3 days | Verified WhatsApp green badge channel, 1,000 conversations/mo. Requires GSTIN.

3. CLOUD & PRODUCTIVITY:
- P16: Cloud Email & Office Suite — ₹125/mo per user | Setup: ₹0 | SLA: 1 day | Custom business email (@yourbrand.com), cloud storage, video meetings.
- P17: Cloud Backup 1 TB — ₹499/mo | Setup: ₹0 | SLA: 1 day | Automatic cloud backup of PCs, accounting (Tally, Vyapar) and documents.
- P18: Website + Domain Starter — ₹299/mo | Setup: ₹0 | SLA: 2 days | Custom domain, 5-page builder, hosting, SSL.
- P19: Cloud POS & Billing — ₹599/mo | Setup: ₹2,500 | SLA: 3 days | GST-ready billing on tablet, UPI/card acceptance, inventory tracking.

4. SECURITY & COMPLIANCE:
- P20: Endpoint Security — ₹99/mo per device | Setup: ₹0 | SLA: 1 day | Anti-ransomware, anti-virus for PCs/laptops.
- P21: Managed Firewall — ₹1,999/mo | Setup: ₹4,000 | SLA: 10 days | Next-gen firewall at the site, managed by Accel SOC. Requires GSTIN, min 10 employees.
- P22: Secure Wi-Fi with Guest Network — ₹399/mo | Setup: ₹1,000 | SLA: 3 days | Separate customer Wi-Fi portal with content filtering.

5. IOT & SMART SURVEILLANCE:
- P23: Cloud CCTV — ₹199/mo per camera | Setup: ₹1,800 | SLA: 4 days | HD camera with 30-day cloud recording and mobile app view.
- P24: Machine Monitoring IoT — ₹149/mo per device | Setup: ₹3,000 | SLA: 10 days | IoT SIM + sensor kit for machine uptime, vibration, power. Requires GSTIN, min 10 employees.
- P25: Fleet Tracker — ₹199/mo per vehicle | Setup: ₹1,500 | SLA: 3 days | GPS tracker with IoT SIM and live tracking dashboard.

DISCOUNTS & VALUE PROPOSITIONS:
- Multi-Product Bundle Discount: 5% off monthly total for 2+ categories.
- Installation Waiver: Free installation (saving ₹1,500 to ₹3,000) when taking broadband + digital add-on.
- 18% GST Input Tax Credit: 100% claimable by registered businesses.
- 99.5% Uptime SLA: Guaranteed high-availability enterprise backbone.
"""

SALES_ASSISTANT_SYSTEM_PROMPT = f"""
You are the elite "Accel Business AI Digital Advisor" for Project Udyam Digital (Accel YTL Hackathon 2026).
Your mission is to provide small businesses across India with instant, consultative, 10-minute digital onboarding.

{CATALOG_CONTEXT}

CRITICAL RULES:
1. ZERO HUMAN DELAY & INSTANT AUTONOMOUS VERIFICATION:
   - Project Udyam Digital has DIRECT API INTEGRATION with the National GSTN, MSME Udyam, and UIDAI registries.
   - NEVER tell the user that "our agents will review your documents", "our team will verify", "it takes 24-48 hours", or "someone will call you to verify".
   - The AI system ITSELF performs instant autonomous verification in milliseconds.
   - When documents are uploaded or confirmed, congratulate the customer that verification is 100% COMPLETE & APPROVED autonomously with zero paperwork and zero human delays!

2. CONSULTATIVE QUESTIONING & METRICS ANALYSIS (FROM SMB LEADS DATA):
   Before recommending a plan, guide the user through the key metrics:
   - Category 1: Basic Details (Always Established): Business type/segment, staff/employee count, number of sites/branches.
   - Category 2: Required Operational Details: Current internet setup (Mobile hotspot vs Broadband vs Leased line), key daily bottlenecks (UPI failure, customer calls, GST billing, cloud backup), and GSTIN / Udyam registration status.
   - Category 3: Additional Contextual Queries: Sizing add-ons based on business type (e.g. UPI volume for Kirana -> POS & 4G Failover; appointment scheduling for Clinics -> Cloud PBX & Cloud Backup; multi-site branches -> SD-WAN & 1800 number; factory -> Leased line & IoT sensors).

3. STRICT CATALOG GROUNDING & PERSUASIVE EXPLANATION:
   - Recommend ONLY products from the official 25 products above.
   - When explaining products, explain the exact daily business value (e.g. why 4G Failover prevents UPI loss when broadband cables are cut, why Cloud POS automates GST invoices, how 18% GST input credit reduces net cost).
   - If the user has price hesitation, highlight the 5% bundle discount, free setup/router waiver, and affordable options like Biz Fibre 100 (₹999) or 5G AirFiber (₹899).

4. CLARITY & CLARIFICATION PROTOCOL:
   - Always speak clearly, concisely, and warmly.
   - If user input is ambiguous or unclear, politely ask for clarification with 2-3 concrete choices. Never guess blindly.

5. INTENT DETECTION & ACTIONS:
   - If user says "continue with onboarding", "proceed", "start kyc", "ready to buy", "haan shuru karo", set action: "START_ONBOARDING".
   - If user says "wait", "hold on", "pause", "stop", "ruk jao", "not now", set action: "PAUSE_ONBOARDING".
   - If user asks questions or asks to explain, set action: "ANSWER_QUERY".
   - If user provides business details, recommend the tailored grounded bundle and set action: "RECOMMEND_BUNDLE".

OUTPUT FORMAT:
Always return a VALID JSON object adhering to this schema:
{{
  "reply_text": "Markdown formatted sales response...",
  "action": "START_ONBOARDING" | "PAUSE_ONBOARDING" | "ANSWER_QUERY" | "RECOMMEND_BUNDLE" | "CLARIFY" | "NONE",
  "recommended_pids": ["P01", "P07", "P19"],
  "bundle_summary": {{
    "total_monthly": 1897,
    "setup_fee": 0,
    "highlight": "Biz Fibre 100 + Business Postpaid + Cloud POS"
  }}
}}
"""

class GeminiSalesService:
    @staticmethod
    def call_gemini(prompt: str, system_instruction: str = SALES_ASSISTANT_SYSTEM_PROMPT, response_json: bool = True, max_retries: int = 2) -> Optional[Dict[str, Any]]:
        api_key = get_gemini_api_key()
        if not api_key:
            return None
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]}
        }
        if response_json:
            payload["generationConfig"] = {"response_mime_type": "application/json"}
        
        for attempt in range(max_retries + 1):
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=12) as res:
                    data = json.loads(res.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    if response_json:
                        return json.loads(text)
                    return {"text": text}
            except urllib.error.HTTPError as he:
                if he.code in [503, 429] and attempt < max_retries:
                    time.sleep(1.0 * (attempt + 1))
                    continue
                print(f"[GeminiSalesService] HTTP Error {he.code}: {he}")
                break
            except Exception as e:
                print(f"[GeminiSalesService] Gemini call error: {e}")
                if attempt < max_retries:
                    time.sleep(1.0)
                    continue
                break
        return None

    @staticmethod
    def process_sales_conversation(
        session_id: str,
        user_message: str,
        history: List[Dict[str, str]],
        current_bundle: Optional[Dict[str, Any]] = None,
        profile: Optional[Dict[str, Any]] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Uses Gemini 2.5 Flash to generate persuasive, accurate, grounded sales advisor answers,
        detect onboarding readiness, and structure bundles.
        """
        history_str = "\n".join([f"{h.get('role', 'user').upper()}: {h.get('content', '')}" for h in history[-6:]])
        bundle_str = json.dumps(current_bundle or {}, indent=2)
        profile_str = json.dumps(profile or {}, indent=2)
        
        prompt = f"""
CONVERSATION HISTORY:
{history_str}

CUSTOMER JUST SAID: "{user_message}"
PREFERRED LANGUAGE: {language}

CURRENT KNOWN BUSINESS PROFILE:
{profile_str}

CURRENT ACTIVE BUNDLE IN CART (IF ANY):
{bundle_str}

Important Reminders:
- NEVER say human agents will review or verify documents. Autonomous AI verifies instantly via national registries.
- If customer's response is unclear, ask for clarification politely with 2-3 examples.
- If customer says "continue with onboarding" / "proceed" / "start kyc", set action: "START_ONBOARDING".
- If customer says "wait" / "stop" / "pause", set action: "PAUSE_ONBOARDING".
- If customer asks questions, explain benefit-by-benefit with uptime SLA, GST tax credit, and ROI.

Provide the best sales advisor response adhering to the JSON schema.
"""
        result = GeminiSalesService.call_gemini(prompt)
        if result and isinstance(result, dict) and "reply_text" in result:
            return result
        
        return GeminiSalesService._rule_based_sales_fallback(user_message, current_bundle, language)

    @staticmethod
    def _rule_based_sales_fallback(user_message: str, current_bundle: Optional[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Graceful fallback when API key is missing or network drop occurs."""
        lower = user_message.lower()
        if any(w in lower for w in ["onboard", "proceed", "continue", "start", "buy", "kyc", "ready", "shuru"]):
            return {
                "reply_text": "Excellent choice! Initiating **Autonomous Smart KYC**. Our AI connects directly with the National GSTN & MSME Registries for instant digital verification with zero paperwork and zero human delays.\n\nPlease confirm your statutory DPDP Act consent below and upload your document photo or enter details to activate.",
                "action": "START_ONBOARDING",
                "recommended_pids": []
            }
        elif any(w in lower for w in ["wait", "stop", "hold", "pause", "not now", "ruk"]):
            return {
                "reply_text": "Understood! We have paused the onboarding process. Take your time to review. What specific tools or pricing would you like to explore further?",
                "action": "PAUSE_ONBOARDING",
                "recommended_pids": []
            }
        elif any(w in lower for w in ["explain", "detail", "what", "kya", "why", "difference"]):
            return {
                "reply_text": "Here is why this bundle is specifically built for your business:\n\n• **Accel Biz Fibre**: Guarantees symmetric high-speed connectivity so UPI payments, inventory billing, and customer Wi-Fi never fail.\n• **4G/5G Wireless Failover**: If outdoor fiber cables ever get cut, your router pivots instantly to cellular data without dropping a single transaction.\n• **Autonomous Instant Activation**: Connected directly with national registries for 10-minute digital setup.\n\nWould you like to proceed with digital onboarding or customize these tools?",
                "action": "ANSWER_QUERY",
                "recommended_pids": []
            }
        else:
            return {
                "reply_text": "I want to make sure I recommend the most cost-effective plan—could you please clarify if you primarily need high-speed Wi-Fi for UPI billing, customer calling, or multi-site branch connectivity?",
                "action": "CLARIFY",
                "recommended_pids": []
            }

    @staticmethod
    def extract_document_with_gemini(image_bytes: bytes, mime_type: str, doc_type: str) -> Dict[str, Any]:
        """
        Multimodal Vision OCR powered by Gemini 2.5 Flash.
        Extracts structured fields from uploaded document images directly in the cloud.
        """
        api_key = get_gemini_api_key()
        if not api_key:
            return {"valid": False, "error": "GEMINI_API_KEY_NOT_CONFIGURED"}
        
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        prompt = f"""
Analyze this Indian business KYC document ({doc_type}).
Extract all visible fields with high precision:
- For GST Certificate: gstin (15 chars, note that 4th char of embedded PAN may be 'X' in hackathon test data), business_name (or legal name / trade name), address, status (Active/Cancelled), issue_date (YYYY-MM-DD).
- For Udyam Certificate: udyam_number (UDYAM-XX-00-XXXXXXX), enterprise_name, enterprise_type (Micro/Small/Medium), date_of_registration (YYYY-MM-DD), address.
- For Address Proof (Electricity / Utility / Landline / Bank): bill_date (YYYY-MM-DD), consumer_name, provider_name, address.
- For Signatory ID (PAN / Aadhaar): signatory_name, id_number (PAN: ABCDE1234F or Aadhaar 12 digits), date_of_birth.

Also check if the document is incomplete, blank, unreadable, or obscured.

OUTPUT JSON:
{{
  "doc_type": "{doc_type}",
  "is_complete": true,
  "gstin": "...",
  "udyam_number": "...",
  "signatory_name": "...",
  "enterprise_name": "...",
  "address": "...",
  "bill_date": "YYYY-MM-DD",
  "status_on_doc": "Active" | "Cancelled" | "Unknown",
  "ocr_raw_text": "Brief transcription of the main text"
}}
"""
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": mime_type, "data": b64_image}}
                ]
            }],
            "generationConfig": {"response_mime_type": "application/json"}
        }
        
        for attempt in range(2):
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=15) as res:
                    data = json.loads(res.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(text)
            except Exception as e:
                print(f"[GeminiSalesService] Multimodal OCR error attempt {attempt+1}: {e}")
                time.sleep(1.0)
        return {"valid": False, "error": "OCR extraction failed"}
