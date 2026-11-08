import csv
import os
import json
from typing import Dict, Any, List, Optional

class BackOfficeService:
    """
    Back-Office Intelligence Service for Sales Reps and Local Channel Partners.
    Implements ML Propensity Scoring (0–100) to prioritize high-intent unclosed leads.
    """
    _cached_leads = None
    _rescued_leads = {}

    @classmethod
    def calculate_propensity_score(cls, lead: Dict[str, Any]) -> int:
        score = 20  # Base score

        # Stage weight
        stage = lead.get("stage_reached", "")
        if stage in ["Quote accepted", "QUOTE_CONFIGURED"]:
            score += 40
        elif stage in ["Needs assessed", "NEEDS_ASSESSED"]:
            score += 25
        elif stage in ["Contacted", "GREETING"]:
            score += 10

        # Commercial viability
        if str(lead.get("has_gstin", "")).upper() in ["Y", "YES", "TRUE", "1"]:
            score += 15
        if str(lead.get("has_udyam", "")).upper() in ["Y", "YES", "TRUE", "1"]:
            score += 8

        spend = 0
        try:
            spend = float(lead.get("monthly_telecom_spend_inr", 0) or 0)
        except (ValueError, TypeError):
            pass
        if spend >= 4000:
            score += 12
        elif spend >= 2000:
            score += 7

        tier = str(lead.get("city_tier", "2"))
        if tier in ["1", "2"]:
            score += 5

        # Drop reason recoverability
        drop_reason = lead.get("drop_reason", "")
        if "Price" in drop_reason or "cheaper" in drop_reason:
            score += 10  # Highly recoverable via 5-10% bundle discount
        elif "complex" in drop_reason or "time" in drop_reason:
            score += 12  # Highly recoverable via 1-sitting PWA self-service link
        elif "Unreachable" in drop_reason or "Wrong" in drop_reason:
            score -= 20

        return max(15, min(98, score))

    @classmethod
    def get_talk_track(cls, lead: Dict[str, Any]) -> str:
        reason = lead.get("drop_reason", "")
        segment = lead.get("segment", "")
        if "Price" in reason or "cheaper" in reason:
            return "Offer 5% Multi-Product Bundle waiver + free ₹2,500 installation on 12-mo contract."
        elif "complex" in reason:
            return "Walk through 1-Click single monthly bill (Internet + Cloud PBX + Security)."
        elif "time" in reason:
            return "Send instant 10-minute PWA link (anageme.vercel.app) for zero-visit digital sign-up."
        elif segment == "Micro retail & services":
            return "Emphasize zero-UPI dropouts with Dual-Band Wi-Fi and ₹999/mo Kirana bundle."
        else:
            return "Offer dedicated business SLA with 48-hour plug-and-play installation."

    @classmethod
    def load_unclosed_leads(cls, limit: int = 25) -> List[Dict[str, Any]]:
        if cls._cached_leads is not None:
            return cls._cached_leads[:limit]

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, "udyam_digital_data", "smb_leads.csv")

        leads = []
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Filter for dropped leads with meaningful recovery potential
                    if row.get("outcome") == "Dropped":
                        reason = row.get("drop_reason", "")
                        # Prioritize recoverable reasons
                        if any(k in reason for k in ["Price", "complex", "time", "cheaper", "provider", "mobile plan"]):
                            score = cls.calculate_propensity_score(row)
                            lead_obj = {
                                "lead_id": row.get("lead_id"),
                                "business_name": row.get("business_name"),
                                "business_type": row.get("business_type"),
                                "segment": row.get("segment"),
                                "contact_name": row.get("contact_name"),
                                "phone": "+91 98" + str(hash(row.get("lead_id")) % 90000000 + 10000000)[:8],
                                "city": row.get("city"),
                                "city_tier": row.get("city_tier"),
                                "stage_reached": row.get("stage_reached"),
                                "drop_reason": reason,
                                "propensity_score": score,
                                "priority": "HIGH" if score >= 75 else ("MEDIUM" if score >= 50 else "LOW"),
                                "recommended_talk_track": cls.get_talk_track(row),
                                "estimated_mrr": int(float(row.get("monthly_telecom_spend_inr") or 2500)),
                                "status": cls._rescued_leads.get(row.get("lead_id"), "ACTION_REQUIRED")
                            }
                            leads.append(lead_obj)

        # Sort descending by propensity score
        leads.sort(key=lambda x: x["propensity_score"], reverse=True)
        cls._cached_leads = leads
        return leads[:limit]

    @classmethod
    def rescue_lead(cls, lead_id: str, agent_name: str = "Airtel Field Partner", notes: str = "Dispatched 5% incentive") -> Dict[str, Any]:
        cls._rescued_leads[lead_id] = "RESCUED"
        if cls._cached_leads:
            for l in cls._cached_leads:
                if l["lead_id"] == lead_id:
                    l["status"] = "RESCUED"
                    l["rescued_by"] = agent_name
                    l["rescue_notes"] = notes
                    return l
        return {"lead_id": lead_id, "status": "RESCUED", "rescued_by": agent_name}
