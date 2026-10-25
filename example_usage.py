from client import SubscriptionKillerClient
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

def main():
    auditor = SubscriptionKillerClient(dormancy_days_threshold=30)
    print("=== SAAS RECURRING SUBSCRIPTION KILLER ===")

    sample_subs = [
        {"name": "Figma Enterprise", "monthly_cost": 45.00, "last_active_days_ago": 2, "frequency": "monthly"},
        {"name": "Obsolete CRM Addon", "monthly_cost": 120.00, "last_active_days_ago": 115, "frequency": "monthly"},
        {"name": "Legacy Cloud Storage", "monthly_cost": 29.99, "last_active_days_ago": 65, "frequency": "monthly"},
        {"name": "Grammarly Business", "monthly_cost": 25.00, "last_active_days_ago": 5, "frequency": "monthly"},
        {"name": "Annual Web Hosting", "monthly_cost": 240.00, "last_active_days_ago": 140, "frequency": "annual"}
    ]

    res = auditor.audit_subscriptions(sample_subs)
    print()
    print(f"Total Annual Burn: ${res['total_annual_burn']} | Recoupable Waste: ${res['potential_annual_savings']} ({res['savings_percentage']}%)")
    print()
    print("Identified Cancellation Recommendations:")
    for item in res['cancellation_candidates']:
        print(f"  - [{item['action_urgency']}] {item['name']}: ${item['monthly_cost']}/mo (${item['annual_cost']}/yr) -> Inactive for {item['days_inactive']} days")

if __name__ == "__main__":
    main()
