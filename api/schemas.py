from pydantic import BaseModel, Field  #( pydantic used for data validation and serialization real time based on the defined schemas)
from typing import List, Dict, Optional


# ----------- Request Schemas -----------

class ExpenseSummaryRequest(BaseModel):
    total_spend: float = Field(..., example=72000000)
    potential_leakage: float = Field(..., example=8900000)
    potential_leakage_pct: float = Field(..., example=12.3)


class ExplainSummaryRequest(BaseModel):
    data: ExpenseSummaryRequest


# ----------- Response Schemas -----------

class ExplainResponse(BaseModel):
    explanation: str


class RecommendationItem(BaseModel):
    vendor: str
    amount: float
    root_cause: str
    recommended_action: str
    priority: str
    estimated_savings: Optional[float]


class AnalysisResponse(BaseModel):
    total_spend: float
    potential_leakage: float
    leakage_pct: float
    top_vendors: List[str]
    recommendations: List[RecommendationItem]
    ai_summary: str
