def simulate_savings(
    total_spend: float,
    potential_leakage: float,
    renegotiation_pct: float,
    subscription_cleanup_pct: float
):
    """
    Simulates optimized spend based on strategic actions.
    """

    renegotiation_savings = potential_leakage * (renegotiation_pct / 100)
    subscription_savings = potential_leakage * (subscription_cleanup_pct / 100)

    total_simulated_savings = renegotiation_savings + subscription_savings
    optimized_spend = total_spend - total_simulated_savings

    return {
        "simulated_savings": round(total_simulated_savings, 2),
        "optimized_spend": round(optimized_spend, 2)
    }