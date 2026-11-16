from pydantic import BaseModel, Field
from typing import List


class IntentOutput(BaseModel):
    """Structured output from Intent Agent"""

    business_question: str = Field(
        description="Original business question"
    )

    metric: str = Field(
        description="Business metric being analyzed"
    )

    dimensions: List[str] = Field(
        description="Dimensions for analysis"
    )

    filters: List[str] = Field(
        description="Filters applied by user"
    )

    time_period: str = Field(
        description="Time period mentioned in query"
    )

    analysis_type: str = Field(
        description="trend, comparison, root_cause, anomaly"
    )

    required_tables: List[str] = Field(
        description="Northwind tables needed"
    )