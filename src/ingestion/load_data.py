import pandas as pd
from pathlib import Path

from src.ingestion.schema import REQUIRED_COLUMNS


DATA_PATH = Path("data/processed/smb_expense_master.csv")


def load_expense_data() -> pd.DataFrame:
    """
    Loads the finalized SMB expense master dataset.

    Returns:
        pd.DataFrame: validated expense data
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Expected data file not found at {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    _validate_schema(df)

    return df


def _validate_schema(df: pd.DataFrame) -> None:
    """
    Ensures the dataset conforms to the expected schema.
    """
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_cols:
        raise ValueError(
            f"Dataset is missing required columns: {missing_cols}"
        )
