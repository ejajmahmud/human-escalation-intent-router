"""Core Human Escalation Intent Router implementation."""
from typing import Dict, Any, Optional, Set


class EscalationVerdict:
    APPROVE_AUTONOMOUS = "APPROVE_AUTONOMOUS"
    REQUIRE_HUMAN_APPROVAL = "REQUIRE_HUMAN_APPROVAL"


class HumanEscalationIntentRouter:
    CRITICAL_ACTIONS = {"delete", "drop", "terminate", "transfer", "pay", "grant_admin", "publish"}

    def __init__(self, min_confidence: float = 0.85, max_cost_autonomous: float = 50.0):
        self.min_confidence = min_confidence
        self.max_cost_autonomous = max_cost_autonomous

    def evaluate(self, action: str, target: str, confidence: float, estimated_cost: float = 0.0) -> Dict[str, Any]:
        action_lower = action.lower()

        # 1. Critical destructive/financial actions
        if any(c in action_lower for c in self.CRITICAL_ACTIONS):
            return {
                "verdict": EscalationVerdict.REQUIRE_HUMAN_APPROVAL,
                "reason": f"Action '{action}' is classified as critical/destructive"
            }

        # 2. Financial cost threshold
        if estimated_cost > self.max_cost_autonomous:
            return {
                "verdict": EscalationVerdict.REQUIRE_HUMAN_APPROVAL,
                "reason": f"Estimated cost (${estimated_cost}) exceeds autonomous limit (${self.max_cost_autonomous})"
            }

        # 3. Model uncertainty
        if confidence < self.min_confidence:
            return {
                "verdict": EscalationVerdict.REQUIRE_HUMAN_APPROVAL,
                "reason": f"Model confidence ({confidence:.2f}) below safe threshold ({self.min_confidence})"
            }

        return {
            "verdict": EscalationVerdict.APPROVE_AUTONOMOUS,
            "reason": "Action meets all autonomous execution policies"
        }
