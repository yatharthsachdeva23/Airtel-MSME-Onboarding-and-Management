import os
import sys
import unittest
from datetime import date

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.kyc_service import KYCService
from backend.dpdp_compliance import DPDPComplianceEngine

class TestKYCValidationAndDPDP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kyc = KYCService()

    def test_approved_applicant_dossiers(self):
        """Applicants K02, K03, K07, K08, K09, K10 must pass registry verification."""
        for app_id in ["K02", "K03", "K07", "K08", "K09", "K10"]:
            result = self.kyc.audit_applicant_dossier(app_id)
            self.assertEqual(
                result["overall_status"],
                "APPROVED",
                f"Applicant {app_id} unexpectedly failed with flags: {result['flags']}"
            )
            self.assertEqual(len(result["flags"]), 0)

    def test_planted_expired_address_proof_k11(self):
        """Applicant K11 has an address proof dated Oct 2025 (>90 days from benchmark 2026-07-15)."""
        result = self.kyc.audit_applicant_dossier("K11")
        self.assertEqual(result["overall_status"], "ACTION_REQUIRED")
        flag_codes = [f["error_code"] for f in result["flags"]]
        self.assertIn("ERROR_ADDRESS_PROOF_EXPIRED", flag_codes)
        
        expired_flag = next(f for f in result["flags"] if f["error_code"] == "ERROR_ADDRESS_PROOF_EXPIRED")
        self.assertGreater(expired_flag["days_old"], 90)
        self.assertIn("mitigation", expired_flag)

    def test_planted_cancelled_gstin_k01(self):
        """Applicant K01 has a Cancelled GSTIN status in the official GSTN registry."""
        result = self.kyc.audit_applicant_dossier("K01")
        self.assertEqual(result["overall_status"], "ACTION_REQUIRED")
        flag_codes = [f["error_code"] for f in result["flags"]]
        self.assertIn("ERROR_GSTIN_INACTIVE", flag_codes)

        inactive_flag = next(f for f in result["flags"] if f["error_code"] == "ERROR_GSTIN_INACTIVE")
        self.assertEqual(inactive_flag["status"].upper(), "CANCELLED")

    def test_planted_incomplete_doc_k04(self):
        """Applicant K04 uploaded a corrupted/incomplete blank GST certificate."""
        result = self.kyc.audit_applicant_dossier("K04")
        self.assertEqual(result["overall_status"], "ACTION_REQUIRED")
        flag_codes = [f["error_code"] for f in result["flags"]]
        self.assertIn("ERROR_DOCUMENT_INCOMPLETE", flag_codes)

    def test_planted_unregistered_gstin_k06(self):
        """Applicant K06 has a fictitious GSTIN not present in the mock GST registry."""
        result = self.kyc.audit_applicant_dossier("K06")
        self.assertEqual(result["overall_status"], "ACTION_REQUIRED")
        flag_codes = [f["error_code"] for f in result["flags"]]
        self.assertIn("ERROR_GSTIN_NOT_FOUND", flag_codes)

    def test_dpdp_consent_notice_generation(self):
        """DPDP Engine generates Section 5 transparent notice with lawful purposes and rights."""
        notice = DPDPComplianceEngine.generate_consent_notice("Ganesh Woodcraft", "Joseph Singh")
        self.assertEqual(notice["data_fiduciary"], "Bharti Airtel Limited (Enterprise Services)")
        self.assertTrue(notice["consent_required"])
        self.assertIn("KYC_VERIFICATION", notice["purposes"])
        self.assertGreater(len(notice["rights"]), 2)

    def test_dpdp_consent_recording(self):
        """DPDP affirmative consent generates non-repudiable cryptographic audit token."""
        record = DPDPComplianceEngine.record_consent("session_123", "Joseph Singh", True, "192.168.1.50")
        self.assertEqual(record["status"], "VALID_CONSENT")
        self.assertTrue(record["consent_granted"])
        self.assertIsNotNone(record["consent_token"])
        self.assertEqual(len(record["consent_token"]), 64)  # SHA-256 hex string

    def test_dpdp_pii_masking(self):
        """PII masking protects PAN, Aadhaar, GSTIN, and Phone numbers in logs and UI."""
        # Aadhaar
        masked_aadhaar = DPDPComplianceEngine.mask_aadhaar("9876 5432 1098")
        self.assertEqual(masked_aadhaar, "XXXX-XXXX-1098")

        # PAN
        masked_pan = DPDPComplianceEngine.mask_pan("ABCDE1234F")
        self.assertEqual(masked_pan, "ABCDE****F")

        # GSTIN
        masked_gstin = DPDPComplianceEngine.mask_gstin("27AABCT3518Q1ZB")
        self.assertEqual(masked_gstin, "27AAB****18Q1ZB")

        # Phone
        masked_phone = DPDPComplianceEngine.mask_phone("+91 9876543210")
        self.assertEqual(masked_phone, "+91 98*** **210")

        # Sanitize customer record
        raw_cust = {
            "name": "Joseph Singh",
            "pan": "ABCDE1234F",
            "aadhaar": "123456789012",
            "phone": "+919876543210",
            "gstin": "27XUIXG0767D1ZP"
        }
        sanitized = DPDPComplianceEngine.sanitize_customer_record(raw_cust)
        self.assertNotIn("pan", sanitized)
        self.assertNotIn("aadhaar", sanitized)
        self.assertEqual(sanitized["pan_masked"], "ABCDE****F")
        self.assertEqual(sanitized["aadhaar_masked"], "XXXX-XXXX-9012")

if __name__ == "__main__":
    unittest.main()
