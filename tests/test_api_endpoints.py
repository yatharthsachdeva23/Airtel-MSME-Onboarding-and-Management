import os
import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "HEALTHY")

    def test_catalog_endpoint(self):
        res = self.client.get("/api/catalog")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["total_products"], 25)

    def test_quote_endpoint(self):
        res = self.client.post("/api/quote", json={
            "product_ids": ["P01", "P07", "P11"],
            "employee_count": 5,
            "num_sites": 1,
            "has_gstin": True,
            "city_tier": 2,
            "billing_cycle_months": 1
        })
        self.assertEqual(res.status_code, 200)
        quote = res.json()
        self.assertTrue(quote["is_valid"])
        self.assertEqual(quote["bundle_discount_percent"], 5)
        self.assertGreater(quote["monthly_total_inr"], 0)

    def test_chat_advisor_endpoint(self):
        res = self.client.post("/api/chat", json={
            "session_id": "test_api_session",
            "message": "We run a grocery store with 3 staff and need fast Wi-Fi and billing",
            "language": "en"
        })
        self.assertEqual(res.status_code, 200)
        chat_resp = res.json()
        self.assertIn("response_text", chat_resp)
        self.assertIn("step", chat_resp)

    def test_kyc_audit_k02_success(self):
        res = self.client.post("/api/kyc/audit-dossier?applicant_id=K02")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["overall_status"], "APPROVED")

    def test_kyc_audit_k11_expired_bill(self):
        res = self.client.post("/api/kyc/audit-dossier?applicant_id=K11")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["overall_status"], "ACTION_REQUIRED")
        flag_codes = [f["error_code"] for f in data["flags"]]
        self.assertIn("ERROR_ADDRESS_PROOF_EXPIRED", flag_codes)

    def test_feasibility_endpoint(self):
        res = self.client.post("/api/feasibility", json={
            "address": "Shop 12, Station Road, Pune",
            "pincode": "411001",
            "requested_product_id": "P01"
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["feasible"])

    def test_live_evals_endpoint(self):
        res = self.client.get("/api/evals/run")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["passed"])
        self.assertEqual(len(data["criteria_evaluated"]), 10)

if __name__ == "__main__":
    unittest.main()
