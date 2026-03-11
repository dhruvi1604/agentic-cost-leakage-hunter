def generate_confidence_timeline(row):
    """
    Generates explainable reasoning steps
    and computes weighted confidence score.

    Confidence logic:
    - Deterministic signals carry higher weight
    - Statistical anomaly alone gives moderate confidence
    - Score capped at 95%
    """

    steps = []
    confidence = 0

    # -------------------------------------------------
    # 1️⃣ Duplicate Detection (Highest Certainty)
    # -------------------------------------------------
    if row.get("duplicate_flag"):
        steps.append(
            "Duplicate transaction pattern detected based on amount and date similarity."
        )
        confidence += 35

    # -------------------------------------------------
    # 2️⃣ Vendor Price Escalation
    # -------------------------------------------------
    if row.get("unit_price_inflation"):
        steps.append(
            "Vendor pricing deviated significantly from historical average."
        )
        confidence += 25

    # -------------------------------------------------
    # 3️⃣ Abnormal Billing Frequency
    # -------------------------------------------------
    if row.get("frequency_spike"):
        steps.append(
            "Transaction frequency exceeded expected behavioral pattern."
        )
        confidence += 20

    # -------------------------------------------------
    # 4️⃣ Subscription Leakage
    # -------------------------------------------------
    if row.get("subscription_leak"):
        steps.append(
            "Recurring subscription pattern appears abnormal."
        )
        confidence += 20

    # -------------------------------------------------
    # 5️⃣ Statistical ML Detection
    # -------------------------------------------------
    if row.get("iforest_anomaly"):
        steps.append(
            "Statistical anomaly detected using Isolation Forest model."
        )
        confidence += 15

    # -------------------------------------------------
    # Fallback
    # -------------------------------------------------
    if not steps:
        steps.append("Minor statistical irregularity detected.")
        confidence = 50

    # Base minimum for any detected anomaly
    confidence = max(confidence, 50)

    # Cap at 95%
    confidence = min(confidence, 95)

    return {
        "steps": steps,
        "confidence": confidence
    }