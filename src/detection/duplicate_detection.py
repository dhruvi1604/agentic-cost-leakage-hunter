import pandas as pd
import numpy as np


def detect_duplicates(
    df: pd.DataFrame,
    amount_tolerance: float = 2.0,
    date_window_days: int = 3
) -> pd.DataFrame:
    """
    Scalable duplicate detection:
    - Exact duplicates
    - Fuzzy duplicates using sliding window (O(n))
    """

    df = df.copy()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    else:
        df["date"] = pd.NaT

    # -------------------------------------------------
    # 1️⃣ Exact duplicates
    # -------------------------------------------------

    if {"vendor", "amount", "date"}.issubset(df.columns):
        df["exact_duplicate"] = df.duplicated(
            subset=["vendor", "amount", "date"],
            keep=False
        )
    else:
        df["exact_duplicate"] = False

    # -------------------------------------------------
    # 2️⃣ Fuzzy duplicates (Sliding Window Approach)
    # -------------------------------------------------

    df["fuzzy_duplicate"] = False

    if not {"vendor", "amount", "date"}.issubset(df.columns):
        df["duplicate_flag"] = df["exact_duplicate"]
        return df

    for vendor, group in df.groupby("vendor"):

        group = group.sort_values("date").reset_index()

        for i in range(len(group) - 1):

            row_a = group.loc[i]
            row_b = group.loc[i + 1]

            if pd.isna(row_a["date"]) or pd.isna(row_b["date"]):
                continue

            # Stop checking if date difference exceeds window
            if abs((row_b["date"] - row_a["date"]).days) > date_window_days:
                continue

            amount_close = abs(row_a["amount"] - row_b["amount"]) <= amount_tolerance

            if amount_close:
                df.loc[
                    [row_a["index"], row_b["index"]],
                    "fuzzy_duplicate"
                ] = True

    # -------------------------------------------------
    # 3️⃣ Final Duplicate Flag
    # -------------------------------------------------

    df["duplicate_flag"] = df["exact_duplicate"] | df["fuzzy_duplicate"]

    return df