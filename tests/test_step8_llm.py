from src.llm.explain import explain_summary

summary = {
    "total_spend": 72000000,
    "potential_leakage": 8900000,
    "confirmed_leakage": 3600000,
    "potential_leakage_pct": 12.3,
}

print(explain_summary(summary))
