from src.features.build_features import build_all_features
from src.detection.anomaly_detection import detect_anomalies
from src.detection.leakage_rules import apply_leakage_rules
from src.detection.duplicate_detection import detect_duplicates
from src.rca.root_cause import assign_root_cause


def run_step5_pipeline():
    print("Loading and building features...")
    df = build_all_features()

    print("Running anomaly detection...")
    df = detect_anomalies(df)

    print("Applying leakage rules...")
    df = apply_leakage_rules(df)

    print("Detecting duplicates...")
    df = detect_duplicates(df)

    print("Assigning root causes...")
    df["root_cause"] = df.apply(assign_root_cause, axis=1)

    print("\nSample anomalies with root causes:\n")
    print(
        df[df["anomaly_flag"] == True][
            ["Vendor", "Amount", "root_cause"]
        ].head(10)
    )

    print(
        "\nTotal anomalies:",
        df["anomaly_flag"].sum()
    )


if __name__ == "__main__":
    run_step5_pipeline()
