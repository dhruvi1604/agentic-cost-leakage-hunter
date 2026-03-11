import pandas as pd
import uuid
from datetime import datetime

#isolation forest doen't not capture all the anomalies, so we need to maintain a memory of anomalies that have been detected and their status. This allows us to track the lifecycle of each anomaly and ensure that we don't miss any important ones.
DEFAULT_STATUS = "new"  # new | reviewed | confirmed | dismissed | recovered


def initialize_anomaly_memory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Initializes memory fields for anomalies.
    """
    df = df.copy()

    if "anomaly_id" not in df.columns:
        df["anomaly_id"] = [str(uuid.uuid4()) for _ in range(len(df))]

    df["status"] = DEFAULT_STATUS
    df["confirmed_savings"] = 0.0
    df["reviewed_at"] = pd.NaT
    df["updated_at"] = datetime.utcnow()

    return df
