# This file defines the canonical expense schema
# It is a CONTRACT, not transformation logic

REQUIRED_COLUMNS = [
    "Source",
    "date",
    "vendor",
    "Category",
    "amount",
    "Units",
    "Unit_Price",
    "PO_ID",
    "Expected_Amount",
    "recurring", 
    "Amount_Delta",
    "Overcharged",
    "High_Value",
]
