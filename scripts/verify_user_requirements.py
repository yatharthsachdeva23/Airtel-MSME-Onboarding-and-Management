import os
import sys
import unittest
import json
import uuid

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.catalog_service import CatalogService
from backend.advisor_engine import AdvisorEngine
from backend.loop_engine import LoopEngine
from backend.ops_service import OpsDashboardService

class TestUserRequirements(unittest.TestCase):
    def setUp(self):
        self.catalog = CatalogService()
        self.loop_engine = LoopEngine()
        self.advisor = AdvisorEngine(self.catalog, self.loop_engine)
        self.session_id = f"test_req_{uuid.uuid4().hex[:8]}"

    def test_no_detected_concern_in_message_and_automatic_agent_transfer(self):
        """
        Req 1 & 3:
        1. No '(Detected concern: ...)' in user-facing message.
        2. Automatic transfer to human agent with clear messaging on dissatisfaction / competitor / objection.
        """
        # Test competitor mention
        res_comp = self.advisor.process_message(self.session_id, "Jio is giving 100 Mbps for Rs 500, this is competitor pricing")
        self.assertNotIn("Detected concern", res_comp["response_text"])
        self.assertNotIn("Routing to nearest partner desk", res_comp["response_text"])
        self.assertTrue(res_comp.get("transferred_to_agent"))
        self.assertIn("Airtel Senior Enterprise Specialist", res_comp["response_text"])

        # Test dissatisfaction query
        session_id_2 = f"test_dissat_{uuid.uuid4().hex[:8]}"
        res_dissat = self.advisor.process_message(session_id_2, "I am not satisfied with these answers, this is unhelpful")
        self.assertNotIn("Detected concern", res_dissat["response_text"])
        self.assertTrue(res_dissat.get("transferred_to_agent"))
        self.assertIn("transferring your request", res_dissat["response_text"])
        self.assertIsNotNone(res_dissat.get("assigned_agent"))

    def test_single_button_start_onboarding_after_quote(self):
        """
        Req 2:
        There should be ONLY ONE button ('Start Onboarding') after the quote is given or let user ask questions.
        """
        sid = f"test_flow_{uuid.uuid4().hex[:8]}"
        # Step 1 -> 2
        r1 = self.advisor.process_message(sid, "Kirana & Retail Store")
        # Step 2 -> 3
        r2 = self.advisor.process_message(sid, "1-3 staff, 1 shop")
        # Step 3 -> 4
        r3 = self.advisor.process_message(sid, "Broadband with 99.5% uptime SLA")
        # Step 4 -> 5 (Quote given!)
        r4 = self.advisor.process_message(sid, "Yes, active GSTIN")
        self.assertEqual(r4["step"], 5)
        self.assertIsNotNone(r4.get("bundle"))
        
        # Verify step 5 quick replies has ONLY ONE BUTTON: 'Start Onboarding'
        qr = r4.get("quick_replies", [])
        self.assertEqual(len(qr), 1, f"Expected exactly 1 button for step 5, got {len(qr)}: {qr}")
        self.assertIn("Start Onboarding", qr[0]["label"])
        self.assertEqual(qr[0]["value"], "Start onboarding")

        # Now test user asking a question at step 5
        r5 = self.advisor.process_message(sid, "can i add more things like upi")
        self.assertEqual(r5["step"], 5)
        qr5 = r5.get("quick_replies", [])
        self.assertEqual(len(qr5), 1, f"Expected exactly 1 button after Q&A, got {len(qr5)}: {qr5}")
        self.assertIn("Start Onboarding", qr5[0]["label"])

    def test_dev_ops_dashboard_data_integrity(self):
        """
        Req 4, 5, 6:
        1. Dev & Ops dashboard shows whole system working properly with all stats.
        2. Live leads transferring to agents (fake data, unique phone numbers, unique suggestions).
        3. Outbound section to call possible leads (unique phone numbers, unique suggestions).
        4. ZERO drop reasons in any lead data!
        5. No duplicate numbers or suggestions across leads!
        """
        dash = OpsDashboardService.get_dashboard_data()
        self.assertTrue(dash["success"])
        self.assertEqual(dash["system_health"]["overall_status"], "OPERATIONAL")
        self.assertGreater(dash["system_health"]["uptime_percentage"], 99.9)

        live_leads = dash["live_lead_transfers"]
        poss_leads = dash["possible_leads_to_call"]
        self.assertGreaterEqual(len(live_leads), 5)
        self.assertGreaterEqual(len(poss_leads), 5)

        all_leads = live_leads + poss_leads
        all_phones = []
        all_suggestions = []

        for lead in all_leads:
            # Strictly NO drop reason!
            self.assertNotIn("drop_reason", lead, f"Found forbidden drop_reason in lead {lead.get('lead_id')}")
            
            # Check phone uniqueness
            phone = lead.get("contact_phone")
            self.assertIsNotNone(phone)
            self.assertNotIn(phone, all_phones, f"Duplicate phone number detected: {phone}")
            all_phones.append(phone)

            # Check suggestion uniqueness
            suggestion = lead.get("tailored_suggestion")
            self.assertIsNotNone(suggestion)
            self.assertNotIn(suggestion, all_suggestions, f"Duplicate suggestion detected: {suggestion}")
            all_suggestions.append(suggestion)

        # Test calling possible lead action
        target_id = poss_leads[0]["lead_id"]
        call_res = OpsDashboardService.call_lead_action(target_id, "Test Agent", "Tested call")
        self.assertTrue(call_res["success"])
        self.assertEqual(call_res["lead"]["call_status"], "CALLED_AND_ENGAGED")

if __name__ == "__main__":
    unittest.main()
