"""Unit tests for human-escalation-intent-router."""
import unittest
from human_escalation_intent_router.router import HumanEscalationIntentRouter, EscalationVerdict


class TestHumanEscalationIntentRouter(unittest.TestCase):
    def test_approve_autonomous(self):
        r = HumanEscalationIntentRouter()
        res = r.evaluate("format_code", "file.py", confidence=0.95)
        self.assertEqual(res["verdict"], EscalationVerdict.APPROVE_AUTONOMOUS)

    def test_escalate_critical(self):
        r = HumanEscalationIntentRouter()
        res = r.evaluate("delete_s3_bucket", "data-lake", confidence=0.99)
        self.assertEqual(res["verdict"], EscalationVerdict.REQUIRE_HUMAN_APPROVAL)

    def test_escalate_uncertain(self):
        r = HumanEscalationIntentRouter(min_confidence=0.8)
        res = r.evaluate("edit_config", "nginx.conf", confidence=0.6)
        self.assertEqual(res["verdict"], EscalationVerdict.REQUIRE_HUMAN_APPROVAL)
