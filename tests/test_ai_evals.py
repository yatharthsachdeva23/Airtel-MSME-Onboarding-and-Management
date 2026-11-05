import os
import sys
import unittest

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.catalog_service import CatalogService
from backend.advisor_engine import AdvisorEngine
from backend.loop_engine import LoopEngine

class TestAIEvalsFramework(unittest.TestCase):
    """
    Automated evaluation test harness verifying the 7 Core AI Criteria
    across 15 distinct MSME benchmark business personas.
    """

    @classmethod
    def setUpClass(cls):
        cls.catalog = CatalogService()
        cls.loop_engine = LoopEngine()
        cls.advisor = AdvisorEngine(cls.catalog, cls.loop_engine)

        # 15 Diverse MSME Test Personas matching realistic judge evaluation scenarios
        cls.test_personas = [
            # 1. Kirana store, 1 site, 2 staff, no GST
            {"id": "P01_Kirana", "segment": "Micro retail & services", "employee_count": 2, "num_sites": 1, "has_gstin": "N", "city_tier": 2},
            # 2. Dental Clinic, 1 site, 4 staff, no GST
            {"id": "P02_Dental", "segment": "Professional offices", "employee_count": 4, "num_sites": 1, "has_gstin": "N", "city_tier": 1},
            # 3. CA Accounting Firm, 1 site, 6 staff, active GST
            {"id": "P03_CA_Firm", "segment": "Professional offices", "employee_count": 6, "num_sites": 1, "has_gstin": "Y", "city_tier": 1},
            # 4. Pharmacy Shop, 1 site, 3 staff, active GST
            {"id": "P04_Pharmacy", "segment": "Micro retail & services", "employee_count": 3, "num_sites": 1, "has_gstin": "Y", "city_tier": 2},
            # 5. Restaurant Chain, 3 branches, 18 staff, active GST
            {"id": "P05_Restaurant_Chain", "segment": "Small multi-site businesses", "employee_count": 18, "num_sites": 3, "has_gstin": "Y", "city_tier": 1},
            # 6. Retail Apparel Chain, 5 branches, 25 staff, active GST
            {"id": "P06_Retail_Chain", "segment": "Small multi-site businesses", "employee_count": 25, "num_sites": 5, "has_gstin": "Y", "city_tier": 2},
            # 7. Small Auto-parts Manufacturer, 1 site, 15 staff, active GST
            {"id": "P07_Auto_Parts", "segment": "Small manufacturers", "employee_count": 15, "num_sites": 1, "has_gstin": "Y", "city_tier": 2},
            # 8. Textile Weaving Unit, 1 site, 8 staff, no GST
            {"id": "P08_Textile_Small", "segment": "Small manufacturers", "employee_count": 8, "num_sites": 1, "has_gstin": "N", "city_tier": 2},
            # 9. Bakery / Cafe, 1 site, 2 staff, no GST
            {"id": "P09_Bakery", "segment": "Micro retail & services", "employee_count": 2, "num_sites": 1, "has_gstin": "N", "city_tier": 1},
            # 10. Coaching Academy, 1 site, 5 staff, active GST
            {"id": "P10_Coaching", "segment": "Professional offices", "employee_count": 5, "num_sites": 1, "has_gstin": "Y", "city_tier": 1},
            # 11. Diagnostic Pathology Lab, 2 sites, 12 staff, active GST
            {"id": "P11_Diagnostic_Lab", "segment": "Professional offices", "employee_count": 12, "num_sites": 2, "has_gstin": "Y", "city_tier": 2},
            # 12. Hardware & Paint Shop, 1 site, 3 staff, no GST
            {"id": "P12_Hardware_Shop", "segment": "Micro retail & services", "employee_count": 3, "num_sites": 1, "has_gstin": "N", "city_tier": 2},
            # 13. Logistics / Courier Hub, 4 branches, 20 staff, active GST
            {"id": "P13_Logistics_Hub", "segment": "Small multi-site businesses", "employee_count": 20, "num_sites": 4, "has_gstin": "Y", "city_tier": 1},
            # 14. Electronics Repair Center, 1 site, 1 staff, no GST
            {"id": "P14_Solo_Shop", "segment": "Micro retail & services", "employee_count": 1, "num_sites": 1, "has_gstin": "N", "city_tier": 2},
            # 15. Heavy Fabrication Unit, 1 site, 30 staff, active GST
            {"id": "P15_Fabrication_Mfg", "segment": "Small manufacturers", "employee_count": 30, "num_sites": 1, "has_gstin": "Y", "city_tier": 1}
        ]

    def test_eval_criterion_1_catalog_groundedness(self):
        """Criterion 1: 100% of recommended product codes must exist in catalog."""
        valid_pids = set(self.catalog.products.keys())
        for persona in self.test_personas:
            rec = self.catalog.recommend_bundle(persona)
            bundle_pids = [item['product_id'] for item in rec['recommended_bundle']]
            for pid in bundle_pids:
                self.assertIn(
                    pid, valid_pids,
                    f"Persona {persona['id']} received hallucinated/invalid product code: {pid}"
                )

    def test_eval_criterion_2_dependency_enforcement(self):
        """Criterion 2: Add-ons requiring base connection must have a valid prerequisite in bundle."""
        for persona in self.test_personas:
            rec = self.catalog.recommend_bundle(persona)
            bundle_pids = [item['product_id'] for item in rec['recommended_bundle']]
            for pid in bundle_pids:
                prod = self.catalog.get_product(pid)
                if prod and prod.requires_one_of:
                    satisfied = any(dep in bundle_pids for dep in prod.requires_one_of)
                    self.assertTrue(
                        satisfied,
                        f"Persona {persona['id']} has product {pid} missing base dependency from {prod.requires_one_of}"
                    )

    def test_eval_criterion_3_gstin_regulatory_guardrail(self):
        """Criterion 3: 0 violations of GSTIN requirements. Non-GST businesses must never get GSTIN-locked products."""
        for persona in self.test_personas:
            if persona['has_gstin'] == 'N':
                rec = self.catalog.recommend_bundle(persona)
                bundle_pids = [item['product_id'] for item in rec['recommended_bundle']]
                for pid in bundle_pids:
                    prod = self.catalog.get_product(pid)
                    self.assertFalse(
                        prod.requires_gstin,
                        f"Regulatory VIOLATION: Non-GST persona {persona['id']} was recommended GSTIN-locked product {pid} ({prod.product_name})"
                    )

    def test_eval_criterion_4_sizing_guardrails(self):
        """Criterion 4: Minimum employee and site thresholds must be strictly respected."""
        for persona in self.test_personas:
            rec = self.catalog.recommend_bundle(persona)
            bundle_pids = [item['product_id'] for item in rec['recommended_bundle']]
            for pid in bundle_pids:
                prod = self.catalog.get_product(pid)
                self.assertGreaterEqual(
                    persona['employee_count'], prod.min_employees,
                    f"Sizing VIOLATION: Persona {persona['id']} with {persona['employee_count']} staff offered product {pid} requiring {prod.min_employees}"
                )
                self.assertGreaterEqual(
                    persona['num_sites'], prod.min_sites,
                    f"Site VIOLATION: Persona {persona['id']} with {persona['num_sites']} sites offered product {pid} requiring {prod.min_sites}"
                )

    def test_eval_criterion_5_arithmetic_quote_accuracy(self):
        """Criterion 5: Pricing calculations must match sum of catalog line items down to the exact rupee."""
        for persona in self.test_personas:
            rec = self.catalog.recommend_bundle(persona)
            quote = rec['quote']

            # Verify math
            calculated_subtotal = sum(item['monthly_cost'] for item in quote['line_items'])
            self.assertEqual(
                calculated_subtotal, quote['monthly_subtotal'],
                f"Arithmetic mismatch on subtotal for persona {persona['id']}"
            )
            expected_tax = round(calculated_subtotal * 0.18, 2)
            self.assertEqual(
                expected_tax, quote['gst_18_pct'],
                f"GST tax calculation mismatch for persona {persona['id']}"
            )
            self.assertEqual(
                round(calculated_subtotal + expected_tax, 2), quote['grand_monthly_total'],
                f"Grand monthly total mismatch for persona {persona['id']}"
            )

    def test_eval_criterion_6_objection_detection_and_handoff(self):
        """Criterion 6: Objection patterns (price, competitor, hesitation) trigger handoff."""
        test_phrases = [
            ("This is too expensive for my kirana shop", "PRICING"),
            ("Local ISP is giving 100 Mbps for Rs 500", "COMPETITOR"),
            ("I need to think about it and call you tomorrow", "HESITATION"),
            ("I want to speak with a human agent to be sure", "TRUST_HUMAN_REQUEST")
        ]
        for phrase, expected_type in test_phrases:
            detection = self.loop_engine.detect_objections(phrase)
            self.assertIsNotNone(detection, f"Failed to detect objection in: '{phrase}'")
            self.assertTrue(detection['detected'])
            self.assertTrue(detection['requires_handoff'])
            self.assertEqual(detection['objections'][0]['type'], expected_type)

    def test_eval_criterion_7_multilingual_flow(self):
        """Criterion 7: Advisor conversational flow functions across multiple Indian languages."""
        for lang in ['en', 'hi', 'ta', 'bn', 'te', 'mr']:
            session_id = f"test_session_{lang}"
            res1 = self.advisor.process_message(session_id, "Kirana shop", language=lang)
            self.assertEqual(res1['step'], 2)
            self.assertIn("response_text", res1)

            res2 = self.advisor.process_message(session_id, "2 staff, 1 shop", language=lang)
            self.assertEqual(res2['step'], 3)

            res3 = self.advisor.process_message(session_id, "Fast UPI Wi-Fi and billing", language=lang)
            self.assertEqual(res3['step'], 4)

            res4 = self.advisor.process_message(session_id, "No GST", language=lang)
            self.assertEqual(res4['step'], 5)
            self.assertIsNotNone(res4['bundle'])
            self.assertTrue(res4['bundle']['validation_passed'])

if __name__ == "__main__":
    unittest.main()
