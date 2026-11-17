from pydantic import BaseModel
from typing import List


class KeyFinding(BaseModel):
    finding: str
    value: str


class Insight(BaseModel):
    insight: str
    business_implication: str


class AnalysisOutput(BaseModel):

    summary: str

    key_findings: List[KeyFinding]

    insights: List[Insight]