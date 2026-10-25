import sys, json
from client import SubscriptionKillerClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    auditor = SubscriptionKillerClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "openclaw-genpark-sub-killer"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    subs = req.get("subscriptions", [])
    res = auditor.audit_subscriptions(subs)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
