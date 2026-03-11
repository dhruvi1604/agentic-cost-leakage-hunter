from src.features.build_features import build_all_features
from src.detection.anomaly_detection import detect_anomalies
from src.detection.leakage_rules import apply_leakage_rules
from src.detection.duplicate_detection import detect_duplicates
from src.rca.root_cause import assign_root_cause
from src.recommendations.savings_estimators import apply_savings_estimation
from src.memory.anomaly_log import initialize_anomaly_memory
from src.memory.metrics import (
    summarize_financials,
    top_vendors_by_leakage,
    monthly_leakage_trend,
    leakage_by_category,
)

def run_step7():
    df = build_all_features()
    df = detect_anomalies(df)
    df = apply_leakage_rules(df)
    df = detect_duplicates(df)

    df["root_cause"] = df.apply(assign_root_cause, axis=1)
    df = apply_savings_estimation(df)
    df = initialize_anomaly_memory(df)

    summary = summarize_financials(df)
    vendors = top_vendors_by_leakage(df)
    monthly = monthly_leakage_trend(df)
    category = leakage_by_category(df)

    print("SUMMARY:", summary)
    print("TOP VENDORS:", list(vendors.items())[:5])
    print("MONTHLY TREND (sample):", list(monthly.items())[:5])
    print("BY CATEGORY (sample):", list(category.items())[:5])

if __name__ == "__main__":
    run_step7()
