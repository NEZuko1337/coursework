from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID

from pydantic import BaseModel


class EnterpriseStatsSchema(BaseModel):
    enterprise_id: int
    investment: float
    profit: float
    roi: float


class InvestmentStatisticsSchema(BaseModel):
    total_investment: float
    total_profit: float
    roi: float
    enterprises: List[EnterpriseStatsSchema]


class OptimizationResultSchema(BaseModel):
    max_profit: float
    distribution: List[float]
    statistics: InvestmentStatisticsSchema


class InvestmentsResultBaseSchema(BaseModel):
    file_name: str
    max_profit: float
    total_investment: float
    roi: float
    distribution: Dict[str, Any]
    enterprise_details: Dict[str, Any]


class InvestmentsResultCreateSchema(InvestmentsResultBaseSchema):
    pass


class InvestmentsResultSchema(InvestmentsResultBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
