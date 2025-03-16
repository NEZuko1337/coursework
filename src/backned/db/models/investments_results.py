from typing import Dict, Any

from sqlalchemy import String, Float
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimeStampMixin


class InvestmentsResult(Base, TimeStampMixin):
    __tablename__ = "investments_results"

    file_name: Mapped[str] = mapped_column(String, nullable=False)
    max_profit: Mapped[float] = mapped_column(Float, nullable=False)
    total_investment: Mapped[float] = mapped_column(Float, nullable=False)
    roi: Mapped[float] = mapped_column(Float, nullable=False)
    distribution: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    enterprise_details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)

    def __repr__(self) -> str:
        return f"<InvestmentResult(id={self.id}, max_profit={self.max_profit})>"
