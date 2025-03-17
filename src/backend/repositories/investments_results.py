import sqlalchemy as sa

from src.backend.db.models.investments_results import InvestmentsResult
from src.backend.repositories.base import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession


class InvestmentsResultRepository(SQLAlchemyRepository):
    model = InvestmentsResult
    
    @classmethod
    async def get_last_investment(cls, async_session: AsyncSession):
        async with async_session() as session:
            query = (sa.select(cls.model)
                     .order_by(cls.model.created_at.desc())
                     .limit(1))
            result = await session.execute(query)
            return result.scalars().first()
