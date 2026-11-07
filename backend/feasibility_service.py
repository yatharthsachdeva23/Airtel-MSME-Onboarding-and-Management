import hashlib
from typing import Dict, Any, Optional

class FeasibilityService:
    """
    GIS and Network Coverage Feasibility Engine for Project Udyam Digital.
    Features:
    - Real-time fiber distribution box (FAT) proximity & capacity check.
    - Automated self-healing pivot to Accel 5G AirFiber FWA when wired fiber is unfeasible.
    - Zero customer drop-off on network constraints.
    """

    MAX_FIBER_DISTANCE_METERS = 250

    @classmethod
    def check_feasibility(cls, address: str, pincode: str, requested_product_id: str = "P01") -> Dict[str, Any]:
        """
        Evaluates physical network feasibility for a customer premise.
        Uses deterministic hashing of address and pincode to simulate real GIS FAT mapping.
        """
        clean_key = f"{pincode.strip()}:{address.strip().lower()}"
        hash_val = int(hashlib.md5(clean_key.encode()).hexdigest(), 16)
        
        # Simulate distance to nearest Fiber Access Terminal (FAT) box
        simulated_distance = 50 + (hash_val % 400)  # Range 50m to 450m
        ports_available = (hash_val % 5) != 0       # 80% have ports available, 20% exhausted

        is_fiber_feasible = (simulated_distance <= cls.MAX_FIBER_DISTANCE_METERS) and ports_available

        # Check if requested product is a wired fiber product (P01, P02, P03, P05)
        is_wired_product = requested_product_id in ["P01", "P02", "P03", "P05"]

        if is_wired_product and not is_fiber_feasible:
            # TRIGGER 5G AIRFIBER AUTO-PIVOT
            unfeasible_reason = (
                f"Nearest fiber terminal is {simulated_distance}m away (exceeds {cls.MAX_FIBER_DISTANCE_METERS}m limit)"
                if simulated_distance > cls.MAX_FIBER_DISTANCE_METERS
                else "Nearest fiber splitter ports are fully subscribed"
            )
            return {
                "feasible": True,
                "wired_fiber_feasible": False,
                "auto_pivoted": True,
                "original_product_id": requested_product_id,
                "recommended_product_id": "P04",  # Accel 5G AirFiber for Business
                "pivot_reason": unfeasible_reason,
                "technology": "5G Fixed Wireless Access (AirFiber)",
                "expected_speed": "Up to 100 Mbps ultra-low latency wireless broadband",
                "install_days": 2,  # Faster install than wired fiber (4 days)
                "message": (
                    f"Wired fiber requires civil extension ({unfeasible_reason}). "
                    "We have seamlessly upgraded your quote to Accel 5G AirFiber with instant plug-and-play installation within 48 hours."
                )
            }

        return {
            "feasible": True,
            "wired_fiber_feasible": is_fiber_feasible,
            "auto_pivoted": False,
            "recommended_product_id": requested_product_id,
            "fat_distance_meters": simulated_distance,
            "technology": "Fiber-to-the-Business (FTTH/FTTB)" if is_wired_product else "Wireless/Cloud",
            "install_days": 4 if is_wired_product else 1,
            "message": "Site is 100% network feasible with dedicated gigabit fiber infrastructure."
        }
