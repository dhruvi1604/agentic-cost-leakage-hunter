import pandas as pd
from .canonical_schema import CANONICAL_COLUMNS, REQUIRED_COLUMNS
from .column_aliases import COLUMN_ALIASES


def normalize_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalize column names
    df.columns = [
    c.strip().lower().replace(" ", "_")
    for c in df.columns]

    # -------------------------
    # Alias mapping
    # -------------------------
    rename_map = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in df.columns:
                rename_map[alias] = canonical
                break

    df = df.rename(columns=rename_map)

    # -------------------------
    # Required columns check
    # -------------------------
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # -------------------------
    # Company normalization
    # -------------------------
    df["company_id"] = df["company_id"].astype(str).str.strip()

    # -------------------------
    # Signal availability flags
    # -------------------------
    df["_has_units"] = "units" in df.columns
    df["_has_unit_price"] = "unit_price" in df.columns
    df["_has_recurring"] = "recurring" in df.columns

    # -------------------------
    # Core normalization
    # -------------------------
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["vendor"] = df["vendor"] if "vendor" in df.columns else "Unknown Vendor"
    df["category"] = df["category"] if "category" in df.columns else "Uncategorized"

    # Units (SAFE)
    if "units" in df.columns:
        df["units"] = (
            pd.to_numeric(df["units"], errors="coerce")
            .fillna(1)
            .clip(lower=1)
        )
    else:
        df["units"] = 1

    # Unit price (SAFE)
    if "unit_price" in df.columns:
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    else:
        df["unit_price"] = df["amount"] / df["units"]

    # Recurring (SAFE)
    if "recurring" in df.columns:
        df["recurring"] = df["recurring"].fillna(False).astype(bool)
    else:
        df["recurring"] = False

    # Expected amount (neutral)
    df["expected_amount"] = df.get("expected_amount", df["amount"])

    # Derived signals
    df["amount_delta"] = df["amount"] - df["expected_amount"]
    df["overcharged"] = df["amount_delta"] > 0
    df["high_value"] = df["amount"] > df["amount"].quantile(0.99)

    # -------------------------
    # Guarantee canonical schema
    # -------------------------
    for col in CANONICAL_COLUMNS:
        if col not in df.columns:
            df[col] = None

    return df[CANONICAL_COLUMNS]