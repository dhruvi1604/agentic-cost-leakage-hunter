from fastapi import FastAPI, UploadFile, File
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from api.schemas import (
    AnalysisResponse,
    ExplainRequest,
    ExplainResponse,
)
from api.deps import save_uploaded_csv

from src.features.build_features import build_all_features
from src.detection.anomaly_detection import detect_anomalies
from src.detection.leakage_rules import apply_leakage_rules
from src.detection.duplicate_detection import detect_duplicates
from src.rca.root_cause import assign_root_cause
from src.recommendations.savings_estimators import apply_savings_estimation
from src.memory.anomaly_log import initialize_anomaly_memory
from src.memory.metrics import (
    summarize_financials,
    top_vendors_by_leakage,
    leakage_by_category,
)
from src.llm.explain import explain_summary, explain_vendor

app = FastAPI(title="Agentic Cost Leakage Hunter")


# -------------------------------
# MAIN ANALYSIS ENDPOINT
# -------------------------------
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(file: UploadFile = File(...)):
    path = save_uploaded_csv(file)

    # Load user-uploaded data
    df = pd.read_csv(path)

    # Full pipeline (IMPORTANT: pass df)
    df = build_all_features(df)
    df = detect_anomalies(df)
    df = apply_leakage_rules(df)
    df = detect_duplicates(df)
    df["root_cause"] = df.apply(assign_root_cause, axis=1)
    df = apply_savings_estimation(df)
    df = initialize_anomaly_memory(df)

    return AnalysisResponse(
        summary=summarize_financials(df),
        top_vendors=top_vendors_by_leakage(df),
        leakage_by_category=leakage_by_category(df),
    )


# -------------------------------
# GENAI: SUMMARY EXPLANATION
# -------------------------------
@app.post("/summary/explain", response_model=ExplainResponse)
def explain_summary_api(req: ExplainRequest):
    explanation = explain_summary(req.data)
    return ExplainResponse(explanation=explanation)


# -------------------------------
# GENAI: VENDOR EXPLANATION
# -------------------------------
@app.post("/vendor/explain", response_model=ExplainResponse)
def explain_vendor_api(req: ExplainRequest):
    explanation = explain_vendor(req.data)
    return ExplainResponse(explanation=explanation)
