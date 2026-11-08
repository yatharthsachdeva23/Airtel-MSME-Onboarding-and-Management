import unittest
from backend.backoffice_service import BackOfficeService

class TestBackOfficeService(unittest.TestCase):
    def test_calculate_propensity_score(self):
        lead_high = {
            "stage_reached": "Quote accepted",
            "has_gstin": "Y",
            "has_udyam": "Y",
            "monthly_telecom_spend_inr": "5000",
            "city_tier": "1",
            "drop_reason": "Quote too complex to understand"
        }
        score = BackOfficeService.calculate_propensity_score(lead_high)
        self.assertGreaterEqual(score, 75)

    def test_load_unclosed_leads(self):
        leads = BackOfficeService.load_unclosed_leads(10)
        self.assertGreater(len(leads), 0)
        top = leads[0]
        self.assertIn("lead_id", top)
        self.assertIn("propensity_score", top)
        self.assertIn("recommended_talk_track", top)
        self.assertIn("priority", top)

    def test_rescue_lead(self):
        leads = BackOfficeService.load_unclosed_leads(5)
        if leads:
            lid = leads[0]["lead_id"]
            res = BackOfficeService.rescue_lead(lid, "Airtel Partner Desk", "Applied 10% discount")
            self.assertEqual(res["status"], "RESCUED")

if __name__ == "__main__":
    unittest.main()
