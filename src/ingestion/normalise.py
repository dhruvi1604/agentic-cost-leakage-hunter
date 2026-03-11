import pandas as pd

# Possible column name aliases from real-world data
COLUMN_ALIASES = {
    "date": ["date", "txn_date", "transaction_date", "order_date"],
    "vendor": ["vendor", "merchant", "supplier", "vendor_name"],
    "category": ["category", "expense_category", "item_category"],
    "amount": ["amount", "total", "txn_amount", "expense"],
    "units": ["units", "quantity", "qty"],
    "unit_price": ["unit_price", "price_per_unit", "rate"],
    "po_id": ["po_id", "purchase_order", "document_number"],
    "recurring": ["recurring", "subscription", "is_recurring"],
}


def normalize_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    rename_map = {}

    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in df.columns:
                rename_map[alias] = canonical
                break

    df = df.rename(columns=rename_map)

    # ---- REQUIRED CORE ----
    if "amount" not in df.columns:
        raise ValueError("Amount column is mandatory")

    # ---- OPTIONALS WITH SAFE DEFAULTS ----
    df["vendor"] = df.get("vendor", "Unknown Vendor")
    df["category"] = df.get("category", "Uncategorized")

    if "units" in df.columns:
        df["units"] = pd.to_numeric(df["units"], errors="coerce").fillna(1)
    else:
        df["units"] = 1

    df["po_id"] = df.get("po_id", None)
    df["recurring"] = df.get("recurring", False)

    # Type safety
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df
