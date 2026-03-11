import pandas as pd


def build_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds vendor-level engineered features.
    Assumes canonical schema (lowercase).
    """

    df = df.copy()

    # -------------------------
    # Vendor transaction count
    # -------------------------
    df["vendor_txn_count"] = (
        df.groupby("vendor")["amount"]
        .transform("count")
    )

    # -------------------------
    # Vendor historical mean
    # -------------------------
    df["vendor_amount_mean"] = (
        df.groupby("vendor")["amount"]
        .transform("mean")
    )

    # -------------------------
    # Safe vendor ratio
    # -------------------------
    df["vendor_amount_ratio"] = (
        df["amount"] /
        df["vendor_amount_mean"].replace(0, 1)
    )
    
    df["vendor_mean"] = df.groupby("vendor")["amount"].transform("mean")
    df["vendor_std"] = df.groupby("vendor")["amount"].transform("std")
    
    df["vendor_zscore"] = (
    (df["amount"] - df["vendor_mean"]) /
    df["vendor_std"].replace(0, 1))


    return df