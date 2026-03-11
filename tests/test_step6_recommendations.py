from src.features.build_features import build_all_features
from src.detection.anomaly_detection import detect_anomalies
from src.detection.leakage_rules import apply_leakage_rules
from src.detection.duplicate_detection import detect_duplicates
from src.rca.root_cause import assign_root_cause
from src.recommendations.savings_estimators import apply_savings_estimation
from src.recommendations.recommend import generate_recommendations


def run_step6_pipeline():
    df = build_all_features()
    df = detect_anomalies(df)
    df = apply_leakage_rules(df)
    df = detect_duplicates(df)

    df["root_cause"] = df.apply(assign_root_cause, axis=1)
    df = apply_savings_estimation(df)
    df = generate_recommendations(df)

    print(
        df[df["anomaly_flag"] == True][
            [
                "Vendor",
                "Amount",
                "root_cause",
                "potential_savings",
                "recommended_action",
                "priority",
            ]
        ].head(10)
    )

    print("\nTotal potential savings identified:")
    print(df["potential_savings"].sum())


if __name__ == "__main__":
    run_step6_pipeline()
