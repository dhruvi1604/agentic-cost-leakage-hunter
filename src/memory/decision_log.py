import pandas as pd
from datetime import datetime


def update_anomaly_status(
    df: pd.DataFrame,
    anomaly_id: str,
    new_status: str,
    confirmed_savings: float = 0.0
) -> pd.DataFrame:
    """
    Updates the lifecycle status of an anomaly.
    """
    df = df.copy()

    mask = df["anomaly_id"] == anomaly_id
    if not mask.any():
        return df

    df.loc[mask, "status"] = new_status
    df.loc[mask, "confirmed_savings"] = confirmed_savings
    df.loc[mask, "reviewed_at"] = datetime.utcnow()
    df.loc[mask, "updated_at"] = datetime.utcnow()

    return df
