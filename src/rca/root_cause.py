def assign_root_cause(row) -> str:
    """
    Adaptive root cause labeling.
    Industry-agnostic and context-aware.
    Priority-based logic.
    """

    # 1️⃣ Duplicate Billing
    if row.get("exact_duplicate"):
        return "Duplicate Billing Detected"

    if row.get("fuzzy_duplicate"):
        return "Potential Duplicate Transaction"

    # 2️⃣ Recurring Cost Escalation
    if row.get("subscription_leak"):
        return "Recurring Cost Escalation"

    # 3️⃣ Vendor Price Inflation
    if row.get("unit_price_inflation"):
        return "Vendor Price Escalation"

    # 4️⃣ Billing Frequency Spike
    if row.get("frequency_spike"):
        return "Abnormal Billing Frequency Increase"

    # 5️⃣ High-Value Outlier
    if row.get("high_value_anomaly"):
        return "High-Value Transaction Outlier"

    # 6️⃣ Statistical Pattern Deviation
    if row.get("iforest_anomaly"):
        return "Unusual Spending Pattern Detected"

    return "No Clear Root Cause Identified"