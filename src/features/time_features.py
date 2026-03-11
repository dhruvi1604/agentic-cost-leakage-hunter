import pandas as pd

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    if "date" not in df.columns:
        raise ValueError(
            "Date column missing after normalization. Expected 'date'."
        )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["year_month"] = df["date"].dt.to_period("M")

    return df