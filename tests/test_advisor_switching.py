import os
import sys
import unittest
import uuid

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.catalog_service import CatalogService
from backend.advisor_engine import AdvisorEngine
from backend.loop_engine import LoopEngine

class TestAdvisorSwitching(unittest.TestCase):
    def setUp(self):
        self.catalog = CatalogService()
        self.loop_engine = LoopEngine()
        self.advisor = AdvisorEngine(self.catalog, self.loop_engine)
        self.session_id = f"test_switch_{uuid.uuid4().hex[:8]}"

    def test_business_category_switching_and_dynamic_chips(self):
        # Turn 1: Initial business category
        res1 = self.advisor.process_message(self.session_id, "Kirana & Retail Store")
        self.assertEqual(res1["step"], 2)
        self.assertEqual(res1["profile"]["segment"], "Micro retail & services")
        self.assertTrue(len(res1["quick_replies"]) > 0)
        chip_labels1 = [c["label"] for c in res1["quick_replies"]]
        self.assertTrue(any("1-3 Staff" in l for l in chip_labels1))

        # Turn 2: User switches to Clinic & Pharmacy
        res2 = self.advisor.process_message(self.session_id, "Clinic & Pharmacy")
        self.assertEqual(res2["step"], 2)  # MUST stay on step 2, not advance to step 3!
        self.assertEqual(res2["profile"]["segment"], "Professional offices")
        self.assertIn("Switched your business profile to", res2["response_text"])
        chip_labels2 = [c["label"] for c in res2["quick_replies"]]
        self.assertTrue(any("Doctors" in l or "Clinic" in l for l in chip_labels2))

        # Turn 3: User switches to Logistics & Fleet
        res3 = self.advisor.process_message(self.session_id, "Logistics & Fleet")
        self.assertEqual(res3["step"], 2)  # MUST stay on step 2!
        self.assertEqual(res3["profile"]["segment"], "Small multi-site businesses")
        self.assertIn("Switched your business profile to", res3["response_text"])
        chip_labels3 = [c["label"] for c in res3["quick_replies"]]
        self.assertTrue(any("Hub" in l or "Fleet" in l for l in chip_labels3))

        # Turn 4: User selects sizing for Logistics & Fleet
        res4 = self.advisor.process_message(self.session_id, "4-10 staff, 2 hubs")
        self.assertEqual(res4["step"], 3)
        self.assertEqual(res4["profile"]["employee_count"], 6)
        self.assertEqual(res4["profile"]["num_sites"], 2)

        # Turn 5: User selects internet requirement
        res5 = self.advisor.process_message(self.session_id, "Dedicated Fiber (99.5% SLA)")
        self.assertEqual(res5["step"], 4)
        self.assertEqual(res5["profile"]["current_internet"], "Broadband")

        # Turn 6: User confirms GSTIN
        res6 = self.advisor.process_message(self.session_id, "Yes, Active GSTIN")
        self.assertEqual(res6["step"], 5)
        self.assertEqual(res6["profile"]["has_gstin"], "Y")
        self.assertIsNotNone(res6["bundle"])
        self.assertTrue(res6["bundle"]["validation_passed"])

if __name__ == "__main__":
    unittest.main()
