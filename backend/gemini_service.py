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
    
    # Try reading from .env in workspace root
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
OFFICIAL BHARTI AIRTEL MSME PRODUCT CATALOG (25 PRODUCTS):

1. CONNECTIVITY:
- P01: Biz Fibre 100 — ₹999/mo | Setup: ₹0 | SLA: 5 days | Target: Micro retail, small office | 100 Mbps symmetric broadband, unlimited data, dual-band Wi-Fi.
- P02: Biz Fibre 300 — ₹1,499/mo | Setup: ₹0 | SLA: 5 days | Target: Professional office, clinics, retail | 300 Mbps high-speed, free router.
- P03: Biz Fibre 1G — ₹3,999/mo | Setup: ₹0 | SLA: 7 days | Target: Multi-site, tech startups | 1 Gbps ultra-fast fiber, priority business peering.
- P04: 5G AirFiber for Business — ₹1,199/mo | Setup: ₹1,000 | SLA: 2 days | Target: Micro/small retail where fiber is unavailable | Plug-and-play FWA 5G router.
- P05: Internet Leased Line 20 — ₹8,000/mo | Setup: ₹10,000 | SLA: 21 days | Target: Manufacturing, banks | Dedicated 1:1 unshared bandwidth, 99.5% uptime SLA. Requires GSTIN.
- P06: Internet Leased Line 100 — ₹24,000/mo | Setup: ₹15,000 | SLA: 21 days | Target: Mid-sized factory, IT hubs | 100 Mbps 1:1 symmetric leased line. Requires GSTIN.
- P07: Business Postpaid 299 — ₹299/mo per line | Setup: ₹0 | SLA: 1 day | Unlimited voice, 30GB data, pooled data billing.
- P08: Business Postpaid 499 — ₹499/mo per line | Setup: ₹0 | SLA: 1 day | Unlimited voice, 75GB data, Google Workspace bundle.
- P09: Backup 4G/5G Failover — ₹499/mo | Setup: ₹500 | SLA: 3 days | Automatic wireless failover so billing & UPI payments never go down.
- P10: SD-WAN Branch Connect — ₹2,500/mo per site | Setup: ₹5,000 | SLA: 10 days | Multi-site encrypted mesh networking with central dashboard.

2. VOICE & COLLABORATION:
- P11: Airtel IQ Cloud PBX Basic — ₹499/mo | Setup: ₹1,000 | SLA: 3 days | Smart IVR, 5 virtual extensions, call recording on mobile.
- P12: Airtel IQ Cloud PBX Pro — ₹1,000/mo | Setup: ₹2,000 | SLA: 3 days | Multi-level IVR, CRM integration, 20 extensions.
- P13: Toll-Free 1800 Service — ₹1,500/mo | Setup: ₹2,500 | SLA: 5 days | National 1800 vanity number with intelligent routing.
- P14: SIP Trunk 10 Channels — ₹2,000/mo | Setup: ₹3,000 | SLA: 7 days | Scalable digital voice trunking for existing on-prem PBX.
- P15: WhatsApp Business API — ₹999/mo | Setup: ₹1,500 | SLA: 3 days | Official green badge, bulk marketing broadcasts, automated order alerts.

3. CLOUD & PRODUCTIVITY:
- P16: Google Workspace Starter — ₹125/mo per user | Setup: ₹0 | SLA: 1 day | Custom business email (@yourbrand.com), 30GB Drive, Meet.
- P17: Cloud Backup 100GB — ₹499/mo | Setup: ₹0 | SLA: 1 day | Automated encrypted backup for accounting (Tally, Vyapar) and documents.
- P18: Microsoft 365 Business Basic — ₹145/mo per user | Setup: ₹0 | SLA: 1 day | Web Word, Excel, Teams, 1TB OneDrive cloud storage.
- P19: Cloud POS & Billing — ₹599/mo | Setup: ₹2,500 | SLA: 3 days | Android smart POS, UPI QR soundbox integration, GST invoice generation.

4. SECURITY & COMPLIANCE:
- P20: Endpoint Security — ₹99/mo per device | Setup: ₹0 | SLA: 1 day | Anti-ransomware, anti-phishing protection for PC/laptops.
- P21: Managed Firewall — ₹1,999/mo | Setup: ₹3,000 | SLA: 5 days | Next-gen unified threat management and web filtering.
- P22: Secure DNS & Wi-Fi Protection — ₹399/mo | Setup: ₹0 | SLA: 2 days | Block malicious domains, content filtering, guest portal.

5. IOT & SMART SURVEILLANCE:
- P23: Airtel Safe Cam (Cloud CCTV) — ₹199/mo per camera | Setup: ₹1,500 | SLA: 3 days | 1080p HD camera, night vision, 7-day cloud recording, mobile live stream.
- P24: Machine Monitoring IoT — ₹149/mo per device | Setup: ₹1,000 | SLA: 7 days | Industrial IoT sensor for power, vibration, machine uptime.
- P25: Smart Fleet Tracker — ₹249/mo per vehicle | Setup: ₹500 | SLA: 2 days | Real-time GPS tracking, geofencing, fuel monitoring for trucks/vans.

DISCOUNTS & VALUE PROPOSITIONS:
- Multi-Product Bundle Discount: 5% off monthly total for 2+ categories.
- Installation Waiver: Free installation (saving ₹1,500 to ₹3,000) when taking broadband + digital add-on.
- GST Input Tax Credit: 18% GST is 100% claimable by registered businesses.
- 99.5% Uptime SLA: Guaranteed high-availability with Airtel Enterprise backbone.
- 24/7 Dedicated Support: Specialized MSME care desk, no robotic wait times.
"""

SALES_ASSISTANT_SYSTEM_PROMPT = f"""
You are the elite "Airtel Udyam AI Sales Advisor" for Bharti Airtel's Enterprise MSME division.
Your mission is to help Indian small & medium businesses (Kirana shops, clinics, CA/law offices, transport fleets, restaurants, small manufacturers) modernize their digital infrastructure.

{CATALOG_CONTEXT}

YOUR BEHAVIOR & GUIDELINES:
1. Grounded & Accurate: NEVER recommend products or prices that are not in the 25 official products above.
2. Sales Assistant & Persuasion:
   - When a user asks "What is this explain in detail" or asks about any product, DO NOT repeat a canned template. Instead, explain the products clearly, benefit-by-benefit, and persuasively! Highlight why this specific combination empowers their business (e.g. why 4G Failover stops UPI payment losses during fiber cuts, how Cloud POS automates GST billing, how WhatsApp API boosts repeat orders).
   - Address any price hesitation: explain ROI, 18% GST tax credit, waived installation, and 5% bundle discount. If they want cheaper options, suggest Biz Fibre 100 (₹999) or 5G AirFiber (₹1,199).
3. CLARITY & CLARIFICATION PROTOCOL (CRITICAL):
   - Always speak clearly, concisely, and respectfully.
   - If the user's answer is ambiguous, vague, or not understood (e.g. garbled text, incomplete sentence, unclear requirements, mixed messages), DO NOT guess blindly or assume products randomly!
   - Instead, politely ask for clarification in a warm, encouraging manner with 2-3 concrete options (e.g., "To make sure I recommend the most cost-effective setup for you, could you please clarify whether you primarily need Wi-Fi for UPI & billing, or higher speed for multiple PCs and cameras?").
4. Intent Detection:
   - If the user says "continue with onboarding", "proceed", "let's do kyc", "ready to buy", "sign me up", "start kyc", "haan shuru karo", set `action`: "START_ONBOARDING". Congratulate them and inform them that Smart KYC is starting right now.
   - If the user says "wait", "hold on", "pause", "stop", "ruk jao", "not now", "let me change plan", set `action`: "PAUSE_ONBOARDING". Acknowledge gently that onboarding is paused and ask how you can help.
   - If the user asks a question, explain in detail and set `action`: "ANSWER_QUERY".
   - If the user gives business details (segment, size, needs), recommend the ideal grounded bundle and set `action`: "RECOMMEND_BUNDLE".
5. Formatting:
   - Format with clean, structured markdown. Use `**bold**` for key terms and prices, bullet points `•` for itemized tools, and clear paragraph breaks so the user can read it comfortably on a phone.
6. Multilingual:
   - If the user speaks in Hindi/Hinglish, reply warmly in natural Hindi/Hinglish. If in English, reply in crisp English. Always maintain an encouraging, respectful Indian business tone ("Namaste", "Sir/Madam", "Ji").

OUTPUT FORMAT:
You MUST ALWAYS respond with a VALID JSON object adhering to this schema:
{{
  "reply_text": "Markdown formatted sales response here...",
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

Remember:
- If customer's response is unclear or confusing, ask for clarification politely with 2-3 examples.
- If customer says "continue with onboarding" / "proceed" / "start kyc", set action: "START_ONBOARDING".
- If customer says "wait" / "stop" / "pause", set action: "PAUSE_ONBOARDING".
- If customer asks questions or asks to explain, answer persuasively with exact benefits, uptime SLA, and ROI.

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
                "reply_text": "Excellent choice! Let's get your Airtel digital business account verified and activated. Our Smart KYC takes under 2 minutes with zero physical paperwork.\n\nPlease confirm your DPDP Act consent below and snap a photo of your business document to proceed.",
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
                "reply_text": "Here is why this bundle is specifically built for your business:\n\n• **Airtel Biz Fibre**: Guarantees symmetric high-speed connectivity so UPI payments, inventory billing, and customer Wi-Fi never fail.\n• **4G/5G Wireless Failover**: If outdoor fiber cables ever get cut, your router pivots instantly to cellular data without dropping a single transaction.\n• **24/7 Dedicated Enterprise Support**: Specialized MSME assistance desk with guaranteed 48-hour activation.\n\nWould you like to proceed with digital onboarding or customize these tools?",
                "action": "ANSWER_QUERY",
                "recommended_pids": []
            }
        else:
            return {
                "reply_text": "I want to make sure I get you the best setup—could you please clarify if you primarily need high-speed Wi-Fi for UPI billing, customer calling, or multi-site branch connectivity?",
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
- For GST Certificate: gstin (15 chars), business_name (or legal name / trade name), address, status (Active/Cancelled), issue_date (YYYY-MM-DD).
- For Udyam Certificate: udyam_number (UDYAM-XX-00-XXXXXXX), enterprise_name, enterprise_type (Micro/Small/Medium), date_of_registration (YYYY-MM-DD), address.
- For Address Proof (Electricity / Utility / Landline / Bank): bill_date (YYYY-MM-DD), consumer_name, provider_name, address.
- For Signatory ID (PAN / Aadhaar): signatory_name, id_number (PAN: ABCDE1234F or Aadhaar 12 digits), date_of_birth.

Also check if the document is incomplete, blank, or obscured.

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
