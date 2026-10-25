import sys, datetime
sys.stdout.reconfigure(encoding='utf-8')

class SubscriptionKillerClient:
    """
    SaaS & Personal Recurring Subscription Auditor.
    Analyzes transaction intervals, identifies dormant/ghost subscriptions
    with zero recent engagement, flags price creep, and calculates annual burn.
    """
    def __init__(self, dormancy_days_threshold=45):
        self.dormancy_threshold = dormancy_days_threshold

    def audit_subscriptions(self, subscriptions):
        """
        subscriptions: list of dicts:
        {"name": str, "monthly_cost": float, "last_active_days_ago": int, "frequency": str}
        """
        if not subscriptions:
            return {"status": "error", "message": "No subscriptions provided"}

        total_monthly_spend = 0.0
        ghost_monthly_waste = 0.0
        cancellation_candidates = []

        for sub in subscriptions:
            cost = float(sub.get("monthly_cost", 0.0))
            if sub.get("frequency") == "annual":
                cost = cost / 12.0
            total_monthly_spend += cost

            days_inactive = int(sub.get("last_active_days_ago", 0))
            is_dormant = days_inactive >= self.dormancy_threshold

            urgency = "HIGH_PRIORITY_CANCEL" if days_inactive >= 90 else ("MEDIUM_DORMANT" if is_dormant else "ACTIVE_HEALTHY")

            if is_dormant:
                ghost_monthly_waste += cost
                annual_waste = cost * 12.0
                cancellation_candidates.append({
                    "name": sub["name"],
                    "monthly_cost": round(cost, 2),
                    "annual_cost": round(annual_waste, 2),
                    "days_inactive": days_inactive,
                    "action_urgency": urgency
                })

        annual_burn_total = total_monthly_spend * 12.0
        potential_annual_savings = ghost_monthly_waste * 12.0
        savings_percentage = (potential_annual_savings / annual_burn_total * 100) if annual_burn_total > 0 else 0.0

        return {
            "status": "success",
            "evaluated_subscriptions_count": len(subscriptions),
            "total_monthly_spend": round(total_monthly_spend, 2),
            "total_annual_burn": round(annual_burn_total, 2),
            "potential_annual_savings": round(potential_annual_savings, 2),
            "savings_percentage": round(savings_percentage, 1),
            "cancellation_candidates": cancellation_candidates
        }
