import pandas as pd


class DatasetValidationError(Exception):
    pass


def validate_expense_dataset(df: pd.DataFrame) -> None:
    # --- Rule 1: Basic sanity ---
    if df.empty or df.shape[1] < 2:
        raise DatasetValidationError(
            "Dataset is empty or has too few columns."
        )

    # Normalize column names for detection only
    cols = [c.lower() for c in df.columns]

    # --- Rule 2: Detect amount-like column ---
    numeric_scores = {}

    for col in df.columns:
        series = pd.to_numeric(df[col], errors="coerce")
        non_null_ratio = series.notna().mean()

        if non_null_ratio > 0.7:
            median = series.median()
            if median and median > 0:
                numeric_scores[col] = non_null_ratio

    if not numeric_scores:
        raise DatasetValidationError(
            "No amount-like numeric column detected."
        )

    # --- Rule 3: Detect date-like column ---
    date_candidates = []

    for col in df.columns:
        if any(k in col.lower() for k in ["date", "time", "txn", "invoice"]):
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() > 0.5:
                date_candidates.append(col)

    if not date_candidates:
        raise DatasetValidationError(
            "No date-like column detected."
        )

    # Passed validation
    return
