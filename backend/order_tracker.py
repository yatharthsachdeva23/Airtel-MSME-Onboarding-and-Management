import datetime
import uuid
from typing import Dict, Any, List, Optional

class OrderTrackerService:
    """
    Transparent SLA Milestone Tracker for Project Udyam Digital orders.
    Provides customer-facing real-time visibility into onboarding progress,
    estimated activation timelines, and engineer dispatch statuses.
    """
    _orders = {}

    MILESTONES = [
        {"id": "ORDER_PLACED", "label": "Order Placed", "sla_hours": 0},
        {"id": "KYC_VERIFIED", "label": "Smart KYC Verified", "sla_hours": 1},
        {"id": "FEASIBILITY_LOCKED", "label": "Network Port Reserved", "sla_hours": 2},
        {"id": "ESIGN_COMPLETED", "label": "Digital Agreement Signed", "sla_hours": 4},
        {"id": "DISPATCH_READY", "label": "Hardware / SIM Dispatched", "sla_hours": 24},
        {"id": "ENGINEER_ASSIGNED", "label": "Field Engineer Assigned", "sla_hours": 36},
        {"id": "LIVE_ACTIVATED", "label": "Service Live & Active", "sla_hours": 48}
    ]

    @classmethod
    def create_order(
        cls,
        session_id: str,
        customer_name: str,
        entity_name: str,
        phone: str,
        address: str,
        bundle: Dict[str, Any],
        technology: str = "Fiber",
        install_days: int = 2
    ) -> Dict[str, Any]:
        """
        Creates a new tracked order with SLA calculations.
        """
        order_id = f"AIRTEL-UDYAM-{uuid.uuid4().hex[:6].upper()}"
        now = datetime.datetime.now(datetime.timezone.utc)
        est_activation = now + datetime.timedelta(days=install_days)

        order = {
            "order_id": order_id,
            "session_id": session_id,
            "customer_name": customer_name,
            "entity_name": entity_name,
            "phone": phone,
            "address": address,
            "bundle": bundle,
            "technology": technology,
            "install_days": install_days,
            "created_at": now.isoformat(),
            "estimated_activation": est_activation.strftime("%d %B %Y, %I:%M %p"),
            "current_milestone": "KYC_VERIFIED",
            "progress_percent": 35,
            "tracking_number": f"DELHIVERY-{uuid.uuid4().hex[:8].upper()}",
            "engineer_name": "Ramesh Kumar (Airtel Certified Lead Engineer)",
            "engineer_contact": "+91 98450 12345",
            "milestone_history": [
                {"milestone": "ORDER_PLACED", "timestamp": now.isoformat(), "status": "COMPLETED"},
                {"milestone": "KYC_VERIFIED", "timestamp": now.isoformat(), "status": "COMPLETED"},
                {"milestone": "FEASIBILITY_LOCKED", "timestamp": now.isoformat(), "status": "IN_PROGRESS"},
                {"milestone": "ESIGN_COMPLETED", "timestamp": None, "status": "PENDING"},
                {"milestone": "DISPATCH_READY", "timestamp": None, "status": "PENDING"},
                {"milestone": "ENGINEER_ASSIGNED", "timestamp": None, "status": "PENDING"},
                {"milestone": "LIVE_ACTIVATED", "timestamp": None, "status": "PENDING"}
            ]
        }
        cls._orders[order_id] = order
        return order

    @classmethod
    def get_order(cls, order_id: str) -> Optional[Dict[str, Any]]:
        return cls._orders.get(order_id)

    @classmethod
    def update_milestone(cls, order_id: str, new_milestone: str, progress_percent: int) -> Optional[Dict[str, Any]]:
        order = cls._orders.get(order_id)
        if not order:
            return None
        order["current_milestone"] = new_milestone
        order["progress_percent"] = progress_percent
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        for m in order["milestone_history"]:
            if m["milestone"] == new_milestone:
                m["status"] = "COMPLETED"
                m["timestamp"] = now
        return order
