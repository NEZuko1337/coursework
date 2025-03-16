from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.db.schemas.investments_results import (
    InvestmentsResultCreateSchema, InvestmentsResultSchema)
from src.backend.exceptions import NotFoundError
from src.backend.repositories.investments_results import \
    InvestmentsResultRepository


class InvestmentsResultService:
    @classmethod
    async def get_all_investments(
        cls,
        async_session: AsyncSession,
    ) -> List[InvestmentsResultSchema]:
        result = await InvestmentsResultRepository.get_all(
            async_session=async_session
        )
        if not result:
            return []
        return result

    @classmethod
    async def get_investment_by_id(
        cls,
        async_session: AsyncSession,
        investment_id: UUID,
    ) -> InvestmentsResultSchema:
        result = await InvestmentsResultRepository.get_by_id(
            async_session=async_session,
            id=investment_id,
        )
        if not result:
            raise NotFoundError(f'Запись с {investment_id} не найдена')
        return result

    @classmethod
    async def create_investment(
        cls,
        async_session: AsyncSession,
        data: InvestmentsResultCreateSchema,
    ) -> InvestmentsResultSchema:
        result = await InvestmentsResultRepository.create(
            async_session=async_session,
            data=data.model_dump(),
        )
        return InvestmentsResultSchema.model_validate(result)

    @classmethod
    async def update_investment(
        cls,
        async_session: AsyncSession,
        investment_id: UUID,
        data: InvestmentsResultCreateSchema,
    ):
        result = await InvestmentsResultRepository.update_by_id(
            async_session=async_session,
            id=investment_id,
            data=data.model_dump()
        )
        if not result:
            raise NotFoundError(f'Запись с {investment_id} не найдена')
        return InvestmentsResultSchema.model_validate(result)

    @classmethod
    async def delete_investment(
        cls,
        async_session: AsyncSession,
        investment_id: UUID,
    ):
        investment = await cls.get_investment_by_id(
            async_session=async_session,
            investment_id=investment_id,
        )
        if not investment:
            raise NotFoundError(
                f'Запись с {investment_id} не найдена, невозможно удалить'
            )

        await InvestmentsResultRepository.delete_by_id(
            async_session=async_session,
            id=investment_id,
        )
