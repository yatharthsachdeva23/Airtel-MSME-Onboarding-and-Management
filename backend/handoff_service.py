import datetime
import uuid
from typing import Dict, Any, List, Optional

class LiveHandoffService:
    """
    Manages intelligent human agent handoffs for complex objection handling,
    hesitation recovery, or specialized enterprise negotiation.
    """
    _tickets = {}

    @classmethod
    def create_handoff_ticket(
        cls,
        session_id: str,
        customer_name: str,
        phone: str,
        business_type: str,
        trigger_reason: str,
        detected_objection: Optional[Dict[str, Any]] = None,
        current_cart: Optional[List[Dict[str, Any]]] = None,
        chat_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Creates an enriched context ticket for sales desk / channel partner handoff.
        """
        ticket_id = f"TICK-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        ticket = {
            "ticket_id": ticket_id,
            "session_id": session_id,
            "customer_name": customer_name,
            "phone": phone,
            "business_type": business_type,
            "trigger_reason": trigger_reason,
            "detected_objection": detected_objection or {},
            "current_cart": current_cart or [],
            "chat_summary": [
                f"{m.get('sender', 'user')}: {m.get('text', '')}"
                for m in (chat_history or [])[-5:]
            ],
            "status": "QUEUED",
            "priority": "HIGH" if "PRICE" in trigger_reason.upper() else "MEDIUM",
            "assigned_agent": "Accel MSME Specialist Desk (Priority Desk #4)",
            "created_at": now
        }
        cls._tickets[ticket_id] = ticket
        return ticket

    @classmethod
    def get_ticket(cls, ticket_id: str) -> Optional[Dict[str, Any]]:
        return cls._tickets.get(ticket_id)

    @classmethod
    def list_tickets(cls) -> List[Dict[str, Any]]:
        return list(cls._tickets.values())

    @classmethod
    def resolve_ticket(cls, ticket_id: str, resolution_notes: str) -> bool:
        if ticket_id in cls._tickets:
            cls._tickets[ticket_id]["status"] = "RESOLVED"
            cls._tickets[ticket_id]["resolution_notes"] = resolution_notes
            cls._tickets[ticket_id]["resolved_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            return True
        return False
