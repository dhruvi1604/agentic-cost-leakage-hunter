import pandas as pd
import numpy as np


def apply_leakage_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enterprise-grade leakage detection.
    Combines:
    - Statistical vendor-relative rules
    - Deterministic business overrides
    """

    df = df.copy()

    # =========================================================
    # 1️⃣ Vendor-relative frequency spike
    # =========================================================

    vendor_freq_stats = (
        df.groupby("vendor")["vendor_txn_count"]
        .agg(["mean", "std"])
        .reset_index()
        .rename(columns={
            "mean": "vendor_freq_mean",
            "std": "vendor_freq_std"
        })
    )

    df = df.merge(vendor_freq_stats, on="vendor", how="left")

    df["frequency_spike"] = (
        df["vendor_txn_count"]
        > (df["vendor_freq_mean"] + 2 * df["vendor_freq_std"].fillna(0))
    )

    # =========================================================
    # 2️⃣ Vendor-relative unit price inflation (statistical)
    # =========================================================

    vendor_price_stats = (
        df.groupby("vendor")["vendor_amount_ratio"]
        .agg(["mean", "std"])
        .reset_index()
        .rename(columns={
            "mean": "vendor_price_mean",
            "std": "vendor_price_std"
        })
    )

    df = df.merge(vendor_price_stats, on="vendor", how="left")

    df["unit_price_inflation"] = (
        df["vendor_amount_ratio"]
        > (df["vendor_price_mean"] + 2 * df["vendor_price_std"].fillna(0))
    )

    # =========================================================
    # 3️⃣ Deterministic Azure Spike Override 🔥
    # =========================================================

    # Absolute inflation guardrail (universal rule)
    df["unit_price_inflation"] = (
        df["unit_price_inflation"]
        | (df["vendor_amount_ratio"] > 1.30)
    )

    # # Final inflation flag
    # df["unit_price_inflation"] = (
    #     df["unit_price_inflation_stat"] |
    #     df["unit_price_inflation_rule"]
    # )

    # =========================================================
    # 4️⃣ Subscription Waste (Zoom / Adobe etc.)
    # =========================================================

    df["subscription_leak"] = (
        (df.get("recurring", False) == True)
        & (df["vendor_txn_count"] > df["vendor_freq_mean"].fillna(0))
        & (df["amount"] > 0)
    )

    # =========================================================
    # 5️⃣ Reimbursement Spike (Travel surge etc.)
    # =========================================================

    # df["reimbursement_spike"] = (
    #     (df["vendor"].str.contains("travel", case=False, na=False))
    #     & (df["amount"] > df["amount"].quantile(0.95))
    # )

    # =========================================================
    # 6️⃣ Clean up temp columns
    # =========================================================

    drop_cols = [
        "vendor_freq_mean",
        "vendor_freq_std",
        "vendor_price_mean",
        "vendor_price_std",
        # "unit_price_inflation_stat",
        # "unit_price_inflation_rule"
    ]

    df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)

    return df
