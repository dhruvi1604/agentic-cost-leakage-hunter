import pandas as pd


def generate_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates action recommendations based on root cause.
    """
    df = df.copy()

    recommendations = []
    priority = []

    for _, row in df.iterrows():

        if row.get("exact_duplicate") or row.get("fuzzy_duplicate"):
            recommendations.append("Investigate and recover duplicate payment")
            priority.append("High")

        elif row.get("subscription_leak"):
            recommendations.append("Review subscription usage and cancel if unused")
            priority.append("Medium")

        elif row.get("unit_price_inflation"):
            recommendations.append("Renegotiate pricing or request vendor justification")
            priority.append("High")

        elif row.get("frequency_spike"):
            recommendations.append("Audit vendor billing frequency and contract terms")
            priority.append("Medium")

        elif row.get("high_value_anomaly"):
            recommendations.append("Review approval and justification for high-value spend")
            priority.append("Medium")

        elif row.get("iforest_anomaly"):
            recommendations.append("Investigate unusual transaction pattern")
            priority.append("Low")

        else:
            recommendations.append("No action required")
            priority.append("Low")

    df["recommended_action"] = recommendations
    df["priority"] = priority

    return df