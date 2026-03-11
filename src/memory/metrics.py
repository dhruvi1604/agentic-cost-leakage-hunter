import pandas as pd


def summarize_financials(df: pd.DataFrame) -> dict:
    """
    Enterprise-level financial summary.

    Definitions:
    - Financial Exposure = risk-adjusted exposure estimate
    - Recoverable Savings = conservative estimated savings
    """

    total_spend = df["amount"].sum()

    # Use calculated exposure column (not raw amount)
    financial_exposure = df["financial_exposure"].sum()

    # Conservative recoverable estimate
    recoverable_savings = df["potential_savings"].sum()

    exposure_pct = (
        (financial_exposure / total_spend) * 100
        if total_spend else 0.0
    )

    recoverable_pct = (
        (recoverable_savings / total_spend) * 100
        if total_spend else 0.0
    )

    return {
        "total_spend": round(total_spend, 2),
        "financial_exposure": round(financial_exposure, 2),
        "recoverable_savings": round(recoverable_savings, 2),
        "exposure_pct": round(exposure_pct, 2),
        "recoverable_pct": round(recoverable_pct, 2),
    }


def top_vendors_by_exposure(df: pd.DataFrame, n: int = 10) -> dict:
    """
    Top vendors by risk-adjusted financial exposure.
    """

    s = (
        df[df["anomaly_flag"] == True]
        .groupby("vendor")["financial_exposure"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

    return s.round(2).to_dict()


def top_vendors_by_recoverable(df: pd.DataFrame, n: int = 10) -> dict:
    """
    Top vendors by conservative recoverable savings.
    """

    s = (
        df[df["anomaly_flag"] == True]
        .groupby("vendor")["potential_savings"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

    return s.round(2).to_dict()


def monthly_exposure_trend(df: pd.DataFrame) -> dict:
    """
    Monthly trend of risk-adjusted exposure.
    """

    if "year_month" not in df.columns:
        return {}

    s = (
        df[df["anomaly_flag"] == True]
        .groupby("year_month")["financial_exposure"]
        .sum()
    )

    return s.round(2).astype(float).to_dict()


def exposure_by_category(df: pd.DataFrame) -> dict:
    """
    Exposure grouped by spend category using risk-adjusted exposure.
    """

    s = (
        df[df["anomaly_flag"] == True]
        .groupby("category")["financial_exposure"]
        .sum()
    )

    return s.round(2).to_dict()