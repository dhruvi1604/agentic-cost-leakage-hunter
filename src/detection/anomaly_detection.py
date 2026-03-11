import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# =====================================================
# Dynamic Contamination Estimation (SMB Balanced Mode)
# =====================================================

def _estimate_contamination(n_rows: int) -> float:
    """
    Balanced SMB anomaly rate target: ~4–7%
    """
    if n_rows < 50:
        return 0.06

    estimated = 1 / np.sqrt(n_rows)

    # Bound between 2% and 7%
    return float(min(0.07, max(0.02, estimated)))


# =====================================================
# Main Detection Function
# =====================================================

def detect_anomalies(
    df: pd.DataFrame,
    random_state: int = 42
) -> pd.DataFrame:

    df = df.copy()

    # =====================================================
    # 1️⃣ Feature Selection
    # =====================================================

    candidate_features = [
        "amount",
        "vendor_amount_ratio",
        "frequency_spike",
        "unit_price_inflation",
        "vendor_zscore",
    ]

    feature_cols = [col for col in candidate_features if col in df.columns]

    if not feature_cols:
        raise ValueError("No valid anomaly features found in dataframe.")

    X = (
        df[feature_cols]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
    )

    # =====================================================
    # 2️⃣ Scaling
    # =====================================================

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # =====================================================
    # 3️⃣ Isolation Forest
    # =====================================================

    contamination_rate = _estimate_contamination(len(df))

    model = IsolationForest(
        n_estimators=300,
        contamination=contamination_rate,
        random_state=random_state,
        n_jobs=-1
    )

    model.fit(X_scaled)

    raw_scores = model.decision_function(X_scaled)

    # Normalize IF scores to 0–1 (higher = more anomalous)
    if raw_scores.max() != raw_scores.min():
        normalized_if = (raw_scores.max() - raw_scores) / (raw_scores.max() - raw_scores.min())
    else:
        normalized_if = np.zeros_like(raw_scores)

    df["iforest_score"] = normalized_if

    # =====================================================
    # 4️⃣ Rule-Based Score
    # =====================================================

    rule_score = np.zeros(len(df))

    if "frequency_spike" in df.columns:
        rule_score += df["frequency_spike"].astype(int) * 0.4

    if "unit_price_inflation" in df.columns:
        rule_score += df["unit_price_inflation"].astype(int) * 0.4

    if "subscription_leak" in df.columns:
        rule_score += df["subscription_leak"].astype(int) * 0.2

    # Cap rule score to 1
    rule_score = np.clip(rule_score, 0, 1)

    # =====================================================
    # 5️⃣ High-Value Guardrail Score
    # =====================================================

    if "amount" in df.columns and df["amount"].notna().any():
        threshold = df["amount"].quantile(0.98)
        high_value_score = (df["amount"] > threshold).astype(int) * 0.6
    else:
        high_value_score = np.zeros(len(df))

    # =====================================================
    # 6️⃣ Duplicate Score
    # =====================================================

    if "duplicate_flag" in df.columns:
        duplicate_score = df["duplicate_flag"].astype(int) * 1.0
    else:
        duplicate_score = np.zeros(len(df))

    # =====================================================
    # 7️⃣ Weighted Hybrid Anomaly Score
    # =====================================================

    df["anomaly_score"] = (
        0.45 * normalized_if +
        0.30 * rule_score +
        0.15 * high_value_score +
        0.10 * duplicate_score
    )

    # =====================================================
    # 8️⃣ Dynamic Threshold (Top ~6%)
    # =====================================================

    threshold = df["anomaly_score"].quantile(1 - contamination_rate)
    df["anomaly_flag"] = df["anomaly_score"] >= threshold

    # Individual component flags (for compatibility)
    df["iforest_anomaly"] = normalized_if >= np.quantile(normalized_if, 1 - contamination_rate)
    df["rule_based_anomaly"] = rule_score > 0
    df["high_value_anomaly"] = high_value_score > 0
    df["duplicate_anomaly"] = duplicate_score > 0

    return df