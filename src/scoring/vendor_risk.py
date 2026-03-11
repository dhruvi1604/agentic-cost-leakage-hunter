import pandas as pd
import numpy as np


def calculate_vendor_risk(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates composite Vendor Risk Index (0–100 scale).

    Risk Components:
    - Exposure Intensity (40%)
    - Anomaly Frequency Ratio (30%)
    - Root Cause Diversity (20%)
    - Recurrence Indicator (10%)
    """

    df = df.copy()

    if df.empty or "vendor" not in df.columns:
        return pd.DataFrame()

    # -------------------------------------------------
    # Aggregate Vendor Metrics
    # -------------------------------------------------

    vendor_stats = (
        df.groupby("vendor")
        .agg(
            total_spend=("amount", "sum"),
            total_exposure=("financial_exposure", "sum"),
            anomaly_count=("anomaly_flag", "sum"),
            txn_count=("amount", "count"),
            root_cause_types=("root_cause", "nunique")
        )
        .reset_index()
    )

    if vendor_stats.empty:
        return vendor_stats

    # -------------------------------------------------
    # Derived Metrics
    # -------------------------------------------------

    vendor_stats["exposure_ratio"] = (
        vendor_stats["total_exposure"] /
        vendor_stats["total_spend"].replace(0, np.nan)
    ).fillna(0)

    vendor_stats["anomaly_ratio"] = (
        vendor_stats["anomaly_count"] /
        vendor_stats["txn_count"].replace(0, np.nan)
    ).fillna(0)

    # Recurrence proxy
    vendor_stats["recurrence_flag"] = (
        vendor_stats["anomaly_count"] > 1
    ).astype(int)

    # -------------------------------------------------
    # Normalization (0–1 scale)
    # -------------------------------------------------

    def safe_normalize(series):
        if series.max() == series.min():
            return pd.Series(0.0, index=series.index)
        return (series - series.min()) / (series.max() - series.min())

    exposure_score = safe_normalize(vendor_stats["exposure_ratio"])
    anomaly_score = safe_normalize(vendor_stats["anomaly_ratio"])
    diversity_score = safe_normalize(vendor_stats["root_cause_types"])
    recurrence_score = vendor_stats["recurrence_flag"]

    # -------------------------------------------------
    # Composite Risk Index
    # -------------------------------------------------

    vendor_stats["risk_index"] = (
        (exposure_score * 0.40) +
        (anomaly_score * 0.30) +
        (diversity_score * 0.20) +
        (recurrence_score * 0.10)
    ) * 100

    vendor_stats["risk_index"] = vendor_stats["risk_index"].round(2)

    # -------------------------------------------------
    # Risk Tier Classification
    # -------------------------------------------------

    def classify_risk(score):
        if score >= 70:
            return "High Risk"
        elif score >= 40:
            return "Moderate Risk"
        else:
            return "Low Risk"

    vendor_stats["risk_tier"] = vendor_stats["risk_index"].apply(classify_risk)

    return vendor_stats.sort_values("risk_index", ascending=False)