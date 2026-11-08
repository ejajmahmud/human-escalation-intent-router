"""CLI for human-escalation-intent-router."""
import sys
import argparse
from .router import HumanEscalationIntentRouter


def main():
    parser = argparse.ArgumentParser(description="Human Escalation Intent Router CLI")
    parser.add_argument("--demo", action="store_true", help="Run escalation router demo")
    args = parser.parse_args()

    if args.demo:
        router = HumanEscalationIntentRouter()
        v1 = router.evaluate("read_file", "README.md", confidence=0.98)
        v2 = router.evaluate("drop_table", "users_v2", confidence=0.95)
        v3 = router.evaluate("deploy_cluster", "staging", confidence=0.70)

        print(f"[+] Safe Task: {v1['verdict']}")
        print(f"[*] Destructive Task: {v2['verdict']} ({v2['reason']})")
        print(f"[*] Low-Confidence Task: {v3['verdict']} ({v3['reason']})")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
