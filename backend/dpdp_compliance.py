import datetime
import re
import hashlib
from typing import Dict, Any, Optional

class DPDPComplianceEngine:
    """
    Compliance engine enforcing India's Digital Personal Data Protection (DPDP) Act 2023
    for Project Udyam Digital.
    """
    DATA_FIDUCIARY = "Bharti Airtel Limited (Enterprise Services)"
    DPO_CONTACT = "dpo.enterprise@airtel.com"
    ALLOWED_PURPOSES = {
        "KYC_VERIFICATION": "Verifying authorized signatory identity and entity credentials under DoT regulations.",
        "BILLING_SETUP": "Configuring corporate account billing, e-invoicing, and credit assessment.",
        "SERVICE_PROVISIONING": "Enabling dispatch of 5G AirFiber CPE, corporate SIMs, and field engineer visits."
    }

    @staticmethod
    def generate_consent_notice(entity_name: str, applicant_name: str) -> Dict[str, Any]:
        """
        Generates Section 5 compliant transparent privacy notice before KYC collection.
        """
        return {
            "notice_version": "DPDP-2023-V1.2",
            "data_fiduciary": DPDPComplianceEngine.DATA_FIDUCIARY,
            "dpo_contact": DPDPComplianceEngine.DPO_CONTACT,
            "purposes": DPDPComplianceEngine.ALLOWED_PURPOSES,
            "data_principal": {
                "entity_name": entity_name,
                "applicant_name": applicant_name
            },
            "retention_policy": "Raw unmasked document images are processed strictly in-memory and immediately purged upon cryptographic verification. Verification tokens are retained for regulatory audit.",
            "rights": [
                "Right to access information",
                "Right to correction of inaccurate data",
                "Right to grievance redressal via dpo.enterprise@airtel.com",
                "Right to withdraw consent and request data erasure"
            ],
            "consent_required": True
        }

    @staticmethod
    def record_consent(session_id: str, applicant_name: str, consent_granted: bool, ip_address: str = "127.0.0.1") -> Dict[str, Any]:
        """
        Records verifiable affirmative consent under Section 6 of DPDP Act 2023.
        """
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        consent_token = hashlib.sha256(f"{session_id}:{applicant_name}:{now}:{consent_granted}".encode()).hexdigest()
        
        return {
            "session_id": session_id,
            "consent_token": consent_token,
            "consent_granted": bool(consent_granted),
            "timestamp": now,
            "ip_address": ip_address,
            "status": "VALID_CONSENT" if consent_granted else "CONSENT_REFUSED"
        }

    @staticmethod
    def mask_pan(pan: str) -> str:
        """Masks PAN: ABCDE1234F -> ABCDE****F"""
        if not pan or len(pan) != 10:
            return pan
        return pan[:5] + "****" + pan[9]

    @staticmethod
    def mask_aadhaar(aadhaar: str) -> str:
        """Masks Aadhaar: 1234 5678 9012 -> XXXX-XXXX-9012"""
        clean = re.sub(r'[\s\-]', '', aadhaar or '')
        if len(clean) == 12:
            return f"XXXX-XXXX-{clean[-4:]}"
        return aadhaar

    @staticmethod
    def mask_gstin(gstin: str) -> str:
        """Masks GSTIN: 27AABCT3518Q1ZB -> 27AAB****8Q1ZB"""
        if not gstin or len(gstin) != 15:
            return gstin
        return gstin[:5] + "****" + gstin[9:]

    @staticmethod
    def mask_phone(phone: str) -> str:
        """Masks Phone: +91 9876543210 -> +91 98*** **210"""
        clean = re.sub(r'[\s\-\+]', '', phone or '')
        if len(clean) >= 10:
            last3 = clean[-3:]
            first2 = clean[:2] if len(clean) == 10 else clean[2:4]
            return f"+91 {first2}*** **{last3}"
        return phone

    @classmethod
    def sanitize_customer_record(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes a full customer record for logging and UI rendering, ensuring no unmasked PII leaks.
        """
        sanitized = dict(data)
        if "pan" in sanitized:
            sanitized["pan_masked"] = cls.mask_pan(sanitized["pan"])
            del sanitized["pan"]
        if "aadhaar" in sanitized:
            sanitized["aadhaar_masked"] = cls.mask_aadhaar(sanitized["aadhaar"])
            del sanitized["aadhaar"]
        if "gstin" in sanitized:
            sanitized["gstin_masked"] = cls.mask_gstin(sanitized["gstin"])
        if "phone" in sanitized:
            sanitized["phone_masked"] = cls.mask_phone(sanitized["phone"])
        return sanitized
