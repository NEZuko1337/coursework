
from src.backend.db.models.investments_results import InvestmentsResult
from src.backend.repositories.base import SQLAlchemyRepository


class InvestmentsResultRepository(SQLAlchemyRepository):
    model = InvestmentsResult
