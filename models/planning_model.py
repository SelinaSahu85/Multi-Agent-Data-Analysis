from pydantic import BaseModel
from typing import List


class PlanOutput(BaseModel):
    objective: str
    analysis_steps: List[str]
    required_tables: List[str]
    group_by: List[str]
    required_kpis: List[str]