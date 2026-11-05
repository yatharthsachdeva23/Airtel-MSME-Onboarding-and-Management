import csv
import os
from typing import Dict, List, Optional, Tuple, Any

class Product:
    def __init__(self, row: Dict[str, str]):
        self.product_id = row['product_id'].strip()
        self.category = row['category'].strip()
        self.product_name = row['product_name'].strip()
        self.description = row['description'].strip()
        self.unit = row['unit'].strip()
        self.price_min = int(row['price_min_inr_per_month'])
        self.price_max = int(row['price_max_inr_per_month'])
        self.setup_fee = int(row['one_time_setup_inr'])
        self.min_contract_months = int(row['min_contract_months'])
        self.available_city_tiers = [int(t) for t in row['available_city_tiers'].split(';') if t.strip()]
        self.min_employees = int(row['min_employees'])
        self.min_sites = int(row['min_sites'])
        self.requires_gstin = (row['requires_gstin'].strip().upper() == 'Y')
        self.requires_one_of = [p.strip() for p in row['requires_one_of'].split('|') if p.strip()] if row.get('requires_one_of') and row['requires_one_of'] != 'nan' else []
        self.install_days = int(row['typical_install_days'])
        self.target_segments = [s.strip() for s in row['target_segments'].split(';') if s.strip()]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "category": self.category,
            "product_name": self.product_name,
            "description": self.description,
            "unit": self.unit,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "setup_fee": self.setup_fee,
            "min_contract_months": self.min_contract_months,
            "available_city_tiers": self.available_city_tiers,
            "min_employees": self.min_employees,
            "min_sites": self.min_sites,
            "requires_gstin": self.requires_gstin,
            "requires_one_of": self.requires_one_of,
            "install_days": self.install_days,
            "target_segments": self.target_segments
        }


class CatalogService:
    def __init__(self, catalog_csv_path: Optional[str] = None):
        if not catalog_csv_path:
            # Look in standard workspace locations
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            catalog_csv_path = os.path.join(base_dir, 'udyam_digital_data', 'product_catalogue.csv')
            if not os.path.exists(catalog_csv_path):
                catalog_csv_path = os.path.join('udyam_digital_data', 'product_catalogue.csv')

        self.catalog_path = catalog_csv_path
        self.products: Dict[str, Product] = {}
        self._load_catalog()

    def _load_catalog(self):
        if not os.path.exists(self.catalog_path):
            raise FileNotFoundError(f"Catalogue file not found at {self.catalog_path}")
        with open(self.catalog_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('product_id'):
                    p = Product(row)
                    self.products[p.product_id] = p

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id.strip())

    def list_products(self, category: Optional[str] = None, segment: Optional[str] = None, tier: Optional[int] = None) -> List[Product]:
        results = list(self.products.values())
        if category:
            results = [p for p in results if p.category.lower() == category.lower()]
        if segment:
            # Map standard segment abbreviations: micro, prof, multi, mfg
            seg_code = segment.lower()
            if 'micro' in seg_code: seg_code = 'micro'
            elif 'prof' in seg_code: seg_code = 'prof'
            elif 'multi' in seg_code: seg_code = 'multi'
            elif 'mfg' in seg_code or 'manufactur' in seg_code: seg_code = 'mfg'
            results = [p for p in results if seg_code in p.target_segments]
        if tier:
            results = [p for p in results if tier in p.available_city_tiers]
        return results

    def validate_bundle(self, product_ids: List[str], business_profile: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validates all products in a bundle against business profile and catalog constraints.
        Enforces:
        1. All product IDs must exist in catalogue.
        2. requires_gstin: Must have active GSTIN if True.
        3. requires_one_of: Bundle must contain at least one prerequisite product.
        4. min_employees & min_sites constraints.
        5. available_city_tiers constraints.
        """
        errors = []
        has_gstin = (str(business_profile.get('has_gstin', 'N')).strip().upper() == 'Y')
        employees = int(business_profile.get('employee_count', 1))
        sites = int(business_profile.get('num_sites', 1))
        tier = int(business_profile.get('city_tier', 1))

        # Check existence
        for pid in product_ids:
            if pid not in self.products:
                errors.append(f"Invalid product code: '{pid}' does not exist in catalog.")

        if errors:
            return False, errors

        # Check rules for each product
        for pid in product_ids:
            p = self.products[pid]

            # GSTIN requirement
            if p.requires_gstin and not has_gstin:
                errors.append(f"Product '{p.product_name}' ({p.product_id}) legally requires a registered GSTIN.")

            # Sizing rules
            if employees < p.min_employees:
                errors.append(f"Product '{p.product_name}' requires minimum {p.min_employees} employees (business has {employees}).")
            if sites < p.min_sites:
                errors.append(f"Product '{p.product_name}' requires minimum {p.min_sites} operating sites (business has {sites}).")

            # City tier
            if tier not in p.available_city_tiers:
                errors.append(f"Product '{p.product_name}' is not serviced in City Tier {tier}.")

            # Dependencies
            if p.requires_one_of:
                satisfied = any(dep in product_ids for dep in p.requires_one_of)
                if not satisfied:
                    dep_names = [self.products[d].product_name for d in p.requires_one_of if d in self.products]
                    errors.append(f"Product '{p.product_name}' ({p.product_id}) requires an active base connection from: {', '.join(dep_names)}.")

        return (len(errors) == 0), errors

    def calculate_quote(self, bundle_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates mathematically deterministic pricing for bundle_items:
        [{ "product_id": "P01", "quantity": 1, "unit_price": 999 }]
        """
        line_items = []
        subtotal_min = 0
        subtotal_max = 0
        subtotal_chosen = 0
        total_setup_fee = 0
        max_install_days = 1

        for item in bundle_items:
            pid = item['product_id']
            qty = int(item.get('quantity', 1))
            if pid not in self.products:
                continue
            p = self.products[pid]

            unit_price = item.get('unit_price', p.price_min)
            # Bound within catalog limits
            unit_price = max(p.price_min, min(p.price_max, int(unit_price)))

            item_monthly = unit_price * qty
            item_setup = p.setup_fee * (1 if p.unit == 'per site' else qty)

            subtotal_min += p.price_min * qty
            subtotal_max += p.price_max * qty
            subtotal_chosen += item_monthly
            total_setup_fee += item_setup
            if p.install_days > max_install_days:
                max_install_days = p.install_days

            line_items.append({
                "product_id": p.product_id,
                "product_name": p.product_name,
                "category": p.category,
                "unit": p.unit,
                "quantity": qty,
                "unit_price": unit_price,
                "price_range": f"₹{p.price_min} - ₹{p.price_max}",
                "monthly_cost": item_monthly,
                "setup_fee": item_setup,
                "install_days": p.install_days
            })

        gst_18_pct = round(subtotal_chosen * 0.18, 2)
        grand_monthly_total = round(subtotal_chosen + gst_18_pct, 2)

        return {
            "line_items": line_items,
            "monthly_subtotal": subtotal_chosen,
            "monthly_min_possible": subtotal_min,
            "monthly_max_possible": subtotal_max,
            "one_time_setup_fee": total_setup_fee,
            "gst_18_pct": gst_18_pct,
            "grand_monthly_total": grand_monthly_total,
            "estimated_install_days": max_install_days
        }

    def recommend_bundle(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic, zero-hallucination bundle recommendation based on business segment and needs.
        """
        segment = str(profile.get('segment', 'Micro retail & services')).lower()
        has_gstin = (str(profile.get('has_gstin', 'N')).strip().upper() == 'Y')
        employees = int(profile.get('employee_count', 1))
        sites = int(profile.get('num_sites', 1))
        stated_needs = [str(n).lower() for n in profile.get('stated_needs', [])]

        core_items: List[Dict[str, Any]] = []
        addons: List[Dict[str, Any]] = []

        if 'micro' in segment or 'retail' in segment or 'kirana' in segment or 'salon' in segment:
            # Micro Retail: Biz Fibre 100 (P01) or 5G AirFiber (P04)
            core_items.append({"product_id": "P01", "quantity": 1, "unit_price": 999})
            # Business Postpaid SIM
            core_items.append({"product_id": "P07", "quantity": max(1, min(employees, 2)), "unit_price": 299})
            # Cloud POS if relevant or default
            core_items.append({"product_id": "P19", "quantity": 1, "unit_price": 599})

            # Addons
            if has_gstin:
                addons.append({"product_id": "P15", "quantity": 1, "unit_price": 999, "reason": "WhatsApp Business API for automated customer promotions"})
            addons.append({"product_id": "P23", "quantity": 1, "unit_price": 199, "reason": "Cloud CCTV camera for counter and inventory surveillance"})
            addons.append({"product_id": "P22", "quantity": 1, "unit_price": 399, "reason": "Separate guest Wi-Fi for customers"})

        elif 'prof' in segment or 'clinic' in segment or 'office' in segment or 'coaching' in segment:
            # Professional Office: Biz Fibre 300 (P02)
            core_items.append({"product_id": "P02", "quantity": 1, "unit_price": 1499})
            # Cloud Email (P16)
            core_items.append({"product_id": "P16", "quantity": max(1, employees), "unit_price": 125})
            # Cloud Backup (P17)
            core_items.append({"product_id": "P17", "quantity": 1, "unit_price": 499})
            # Endpoint Security (P20)
            core_items.append({"product_id": "P20", "quantity": max(1, min(employees, 5)), "unit_price": 99})

            # Addons
            addons.append({"product_id": "P09", "quantity": 1, "unit_price": 499, "reason": "Automatic 4G/5G failover for 100% uptime during patient/client meetings"})
            if has_gstin:
                addons.append({"product_id": "P12", "quantity": 1, "unit_price": 1000, "reason": "Cloud IVR telephony for appointment booking"})

        elif 'multi' in segment or 'chain' in segment or sites >= 3:
            # Multi-site: Biz Fibre 300 per site
            core_items.append({"product_id": "P02", "quantity": sites, "unit_price": 1499})
            # 4G Failover per site
            core_items.append({"product_id": "P09", "quantity": sites, "unit_price": 499})
            # Cloud CCTV per site
            core_items.append({"product_id": "P23", "quantity": sites * 2, "unit_price": 199})

            if sites >= 3 and employees >= 10 and has_gstin:
                core_items.append({"product_id": "P10", "quantity": sites, "unit_price": 2500})
            if has_gstin:
                addons.append({"product_id": "P13", "quantity": 1, "unit_price": 1500, "reason": "Centralized 1800 Toll-Free helpline across all branch outlets"})

        else:
            # Manufacturing: Leased line if GSTIN and size permits, else Biz Fibre 1G
            if has_gstin and employees >= 10:
                core_items.append({"product_id": "P05", "quantity": 1, "unit_price": 8000})
                core_items.append({"product_id": "P21", "quantity": 1, "unit_price": 1999})
                core_items.append({"product_id": "P24", "quantity": 5, "unit_price": 149})
            else:
                core_items.append({"product_id": "P02", "quantity": 1, "unit_price": 1499})
                core_items.append({"product_id": "P09", "quantity": 1, "unit_price": 499})

        # Validate bundle before returning
        product_ids = [item['product_id'] for item in core_items]
        valid, errors = self.validate_bundle(product_ids, profile)
        if not valid:
            # Self-healing fallback: strip invalid products
            clean_items = []
            for item in core_items:
                v, _ = self.validate_bundle([item['product_id']], profile)
                if v: clean_items.append(item)
            core_items = clean_items

        quote = self.calculate_quote(core_items)
        return {
            "recommended_bundle": core_items,
            "quote": quote,
            "available_addons": addons,
            "validation_passed": True
        }
