import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.feasibility_service import FeasibilityService
from backend.handoff_service import LiveHandoffService
from backend.order_tracker import OrderTrackerService

class TestPhase3Services(unittest.TestCase):
    def test_fiber_feasibility_check(self):
        """Checks feasibility response structure."""
        res = FeasibilityService.check_feasibility("Shop 14, MG Road, Pune", "411001", "P01")
        self.assertIn("feasible", res)
        self.assertIn("recommended_product_id", res)
        self.assertIn("message", res)

    def test_airfiber_auto_pivot(self):
        """When address hashes to >250m distance, verify auto-pivot to P04 (5G AirFiber)."""
        # Search for an address/pin combination that simulates >250m
        found_pivot = False
        for offset in range(30):
            res = FeasibilityService.check_feasibility(f"Remote Unit {offset}, Sector 99", "110099", "P01")
            if res.get("auto_pivoted"):
                found_pivot = True
                self.assertEqual(res["recommended_product_id"], "P04")
                self.assertEqual(res["technology"], "5G Fixed Wireless Access (AirFiber)")
                self.assertEqual(res["install_days"], 2)
                self.assertIn("AirFiber", res["message"])
                break
        self.assertTrue(found_pivot, "Expected at least one test address to trigger AirFiber auto-pivot.")

    def test_live_handoff_creation_and_resolution(self):
        """Verify objection-triggered handoff ticket creation and resolution."""
        ticket = LiveHandoffService.create_handoff_ticket(
            session_id="sess_abc123",
            customer_name="Sunil Verma",
            phone="+91 98220 11223",
            business_type="Retail Pharmacy",
            trigger_reason="PRICE_OBJECTION",
            detected_objection={"type": "PRICE_SENSITIVITY", "phrase": "pricing is too expensive"},
            current_cart=[{"product_id": "P01", "name": "Airtel Office Internet 100M", "price": 999}],
            chat_history=[{"sender": "user", "text": "Is there any discount? Your price is too high."}]
        )
        self.assertIsNotNone(ticket["ticket_id"])
        self.assertEqual(ticket["status"], "QUEUED")
        self.assertEqual(ticket["priority"], "HIGH")

        # Verify lookup
        fetched = LiveHandoffService.get_ticket(ticket["ticket_id"])
        self.assertEqual(fetched["ticket_id"], ticket["ticket_id"])

        # Resolve ticket
        ok = LiveHandoffService.resolve_ticket(ticket["ticket_id"], "Offered 10% annual billing discount; customer satisfied.")
        self.assertTrue(ok)
        self.assertEqual(LiveHandoffService.get_ticket(ticket["ticket_id"])["status"], "RESOLVED")

    def test_order_tracker_lifecycle(self):
        """Verify order SLA milestone tracker."""
        order = OrderTrackerService.create_order(
            session_id="sess_xyz",
            customer_name="Priya Sharma",
            entity_name="Sharma Medical Diagnostics",
            phone="+91 98450 99887",
            address="Unit 4, Ring Road, Bengaluru - 560001",
            bundle={"monthly_total_inr": 2499, "products": ["P01", "P07", "P08"]},
            technology="5G AirFiber",
            install_days=2
        )
        self.assertIsNotNone(order["order_id"])
        self.assertEqual(order["current_milestone"], "KYC_VERIFIED")
        self.assertIn("DELHIVERY-", order["tracking_number"])

        # Advance milestone
        updated = OrderTrackerService.update_milestone(order["order_id"], "DISPATCH_READY", 65)
        self.assertIsNotNone(updated)
        self.assertEqual(updated["current_milestone"], "DISPATCH_READY")
        self.assertEqual(updated["progress_percent"], 65)

if __name__ == "__main__":
    unittest.main()
