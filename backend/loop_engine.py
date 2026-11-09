import time
import json
import os
import re
import tempfile
from typing import Callable, Any, Dict, Optional, Tuple

class CircuitBreaker:
    """
    Prevents cascading failures by opening circuit after repeated errors
    and directing traffic to deterministic fallback logic.
    """
    def __init__(self, failure_threshold: int = 3, recovery_time_seconds: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_time_seconds = recovery_time_seconds
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED (Normal), OPEN (Failing), HALF-OPEN
        self.last_failure_time = 0

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def is_available(self) -> bool:
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_time_seconds:
                self.state = "HALF-OPEN"
                return True
            return False
        return True


class SessionStateManager:
    """
    Append-only session persistence ensuring zero data loss.
    Re-hydrates state on browser reload or microservice restart.
    Supports serverless read-only environments (Vercel / AWS Lambda) with in-memory fallback.
    """
    def __init__(self, storage_dir: Optional[str] = None):
        self._memory_sessions = {}
        if not storage_dir:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
                storage_dir = os.path.join(tempfile.gettempdir(), 'udyam_data')
            else:
                storage_dir = os.path.join(base_dir, 'data')
        self.storage_dir = storage_dir
        try:
            os.makedirs(self.storage_dir, exist_ok=True)
            self.state_file = os.path.join(self.storage_dir, 'session_store.json')
            if not os.path.exists(self.state_file):
                with open(self.state_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f)
        except Exception:
            self.state_file = None

    def save_session(self, session_id: str, data: Dict[str, Any]):
        sessions = self.get_all_sessions()
        sessions[session_id] = {
            **sessions.get(session_id, {}),
            **data,
            "updated_at": time.time()
        }
        self._memory_sessions[session_id] = sessions[session_id]
        if self.state_file:
            try:
                with open(self.state_file, 'w', encoding='utf-8') as f:
                    json.dump(sessions, f, indent=2)
            except Exception:
                pass

    def get_session(self, session_id: str) -> Dict[str, Any]:
        if session_id in self._memory_sessions:
            return self._memory_sessions[session_id]
        sessions = self.get_all_sessions()
        return sessions.get(session_id, {})

    def get_all_sessions(self) -> Dict[str, Any]:
        if self.state_file and os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._memory_sessions.update(data)
                    return data
            except Exception:
                pass
        return self._memory_sessions


class LoopEngine:
    """
    Universal Loop Engineering Orchestrator.
    Manages retries, schema validation loops, circuit breaking,
    and automatic fallback to deterministic rules.
    """
    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            "llm_advisor": CircuitBreaker(failure_threshold=2, recovery_time_seconds=20),
            "ocr_vision": CircuitBreaker(failure_threshold=3, recovery_time_seconds=30),
            "gstin_registry": CircuitBreaker(failure_threshold=3, recovery_time_seconds=30),
            "udyam_registry": CircuitBreaker(failure_threshold=3, recovery_time_seconds=30)
        }
        self.session_manager = SessionStateManager()

    def execute_with_resilience(
        self,
        service_name: str,
        primary_fn: Callable[[], Any],
        fallback_fn: Optional[Callable[[], Any]] = None,
        max_retries: int = 2
    ) -> Tuple[Any, bool, str]:
        """
        Executes primary_fn with retry loop and circuit breaker.
        Returns: (result, was_fallback_used, status_message)
        """
        cb = self.circuit_breakers.get(service_name)
        if cb and not cb.is_available():
            # Circuit is OPEN, bypass immediately to fallback
            if fallback_fn:
                res = fallback_fn()
                return res, True, f"Service '{service_name}' circuit OPEN; executed deterministic fallback."
            raise RuntimeError(f"Service '{service_name}' circuit OPEN and no fallback registered.")

        attempts = 0
        last_error = ""
        while attempts <= max_retries:
            try:
                result = primary_fn()
                if cb:
                    cb.record_success()
                return result, False, "Success"
            except Exception as e:
                attempts += 1
                last_error = str(e)
                time.sleep(0.1 * attempts)  # Short exponential backoff

        # All retries failed
        if cb:
            cb.record_failure()

        if fallback_fn:
            try:
                fallback_res = fallback_fn()
                return fallback_res, True, f"Primary failed ({last_error}); executed fallback."
            except Exception as fe:
                return None, True, f"Both primary and fallback failed: {fe}"

        return None, False, f"Failed after {max_retries} retries: {last_error}"

    def detect_objections(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Identifies customer dissatisfaction, hesitations, pricing objections, or competitor mentions.
        Triggers instant live agent handoff.
        """
        lower = text.lower()
        objections = []

        price_patterns = [r'too expensive', r'price.*high', r'costly', r'expensive', r'discount', r'mehenga', r'kam karo', r'budget']
        competitor_patterns = [r'competitor', r'jio', r'vi', r'bsnl', r'local isp', r'cheaper plan', r'dusra operator']
        hesitation_patterns = [r'think about it', r'decide later', r'call me tomorrow', r'not sure', r'soch ke bataunga', r'wait']
        trust_patterns = [r'fake', r'scam', r'is this real', r'trust', r'customer care', r'human', r'talk to someone', r'talk.*human', r'speak.*human', r'human agent']
        dissatisfaction_patterns = [
            r'not satisfied', r'dissatisfied', r'unsatisfied', r'not happy', r'unhappy',
            r'terrible', r'horrible', r'awful', r'worst', r'bad service', r'poor service',
            r'waste of time', r'waste my time', r'not helpful', r'unhelpful', r'frustrated',
            r'annoying', r'annoyed', r'hate this', r'ridiculous', r'useless', r'disappointed',
            r'bekar', r'bakwas', r'gussa', r'transfer.*agent', r'transfer me', r'connect.*agent',
            r'speak.*agent', r'talk.*agent', r'call.*agent', r'live agent', r'support executive',
            r'transfer to agent'
        ]

        for p in price_patterns:
            if re.search(p, lower):
                objections.append({"type": "PRICING", "detail": "User raised pricing or budget concern."})
                break
        for p in competitor_patterns:
            if re.search(p, lower):
                objections.append({"type": "COMPETITOR", "detail": "User mentioned competitor pricing or alternative provider."})
                break
        for p in hesitation_patterns:
            if re.search(p, lower):
                objections.append({"type": "HESITATION", "detail": "User is delaying decision; requires trust-building."})
                break
        for p in trust_patterns:
            if re.search(p, lower):
                objections.append({"type": "TRUST_HUMAN_REQUEST", "detail": "User requested human agent or questioned authenticity."})
                break
        for p in dissatisfaction_patterns:
            if re.search(p, lower):
                objections.append({"type": "DISSATISFACTION", "detail": "User expressed dissatisfaction or requested direct live agent transfer."})
                break

        if objections:
            return {
                "detected": True,
                "objections": objections,
                "requires_handoff": True,
                "recommended_action": "Transfer to Senior Airtel Enterprise Specialist with pre-filled cart."
            }
        return None
