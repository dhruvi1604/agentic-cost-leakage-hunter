import pandas as pd


# =====================================================
# Risk-Adjusted + Severity-Weighted Financial Exposure
# =====================================================

def calculate_financial_exposure(row) -> float:

    amount = float(row.get("amount", 0) or 0)

    if not row.get("anomaly_flag"):
        return 0.0

    anomaly_score = float(row.get("anomaly_score", 0.5))

    # Base multiplier by type

    if row.get("duplicate_flag"):
        base_multiplier = 1.0

    elif row.get("unit_price_inflation"):
        base_multiplier = 0.5

    elif row.get("subscription_leak"):
        base_multiplier = 0.6

    elif row.get("frequency_spike"):
        base_multiplier = 0.35

    elif row.get("iforest_anomaly"):
        base_multiplier = 0.25

    else:
        base_multiplier = 0.2

    # Severity-adjusted exposure
    adjusted_multiplier = base_multiplier * anomaly_score

    return round(amount * adjusted_multiplier, 2)


# =====================================================
# Recoverable Savings Estimation
# =====================================================

def estimate_recoverable_savings(row) -> float:

    exposure = float(row.get("financial_exposure", 0) or 0)

    if exposure == 0:
        return 0.0

    if row.get("duplicate_flag"):
        recovery_rate = 0.95

    elif row.get("unit_price_inflation"):
        recovery_rate = 0.6

    elif row.get("subscription_leak"):
        recovery_rate = 0.7

    elif row.get("frequency_spike"):
        recovery_rate = 0.4

    else:
        recovery_rate = 0.3

    return round(exposure * recovery_rate, 2)


# =====================================================
# Apply Estimation
# =====================================================

def apply_savings_estimation(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["financial_exposure"] = df.apply(
        calculate_financial_exposure, axis=1
    )

    df["potential_savings"] = df.apply(
        estimate_recoverable_savings, axis=1
    )

    return df