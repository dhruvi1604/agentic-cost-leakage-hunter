import os

from src.llm.prompts import (
    SYSTEM_PROMPT,
    SUMMARY_PROMPT,
    VENDOR_PROMPT,
    ANOMALY_PROMPT,
)

from src.llm.backends import MockLLM, OpenAILLM, GroqLLM


# =====================================================
# LLM SELECTOR
# =====================================================

def get_llm():

    mode = os.getenv("LLM_MODE", "groq")

    if mode == "openai":
        return OpenAILLM()

    if mode == "groq":
        return GroqLLM()

    return MockLLM()


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def explain_summary(summary: dict) -> str:

    llm = get_llm()

    prompt = SYSTEM_PROMPT + SUMMARY_PROMPT.format(summary=summary)

    return llm.generate(prompt)


# =====================================================
# VENDOR RISK EXPLANATION
# =====================================================

def explain_vendor(vendor_data: dict) -> str:

    llm = get_llm()

    prompt = SYSTEM_PROMPT + VENDOR_PROMPT.format(vendor_data=vendor_data)

    return llm.generate(prompt)


# =====================================================
# ANOMALY EXPLANATION
# =====================================================

def explain_anomaly(transaction: dict, root_cause: str) -> str:

    llm = get_llm()

    prompt = SYSTEM_PROMPT + ANOMALY_PROMPT.format(
        transaction=transaction,
        root_cause=root_cause
    )

    return llm.generate(prompt)