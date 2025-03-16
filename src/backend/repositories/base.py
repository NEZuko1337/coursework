import logging
from abc import ABC
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

Model = TypeVar("Model")


class AbstractRepository(ABC):

    @classmethod
    async def get_by_id(cls, async_session: AsyncSession, id: UUID):
        raise NotImplementedError

    @classmethod
    async def create(cls, async_session: AsyncSession, data: dict):
        raise NotImplementedError

    @classmethod
    async def update_by_id(
        cls,
        async_session: AsyncSession,
        id: UUID,
        data: dict
    ):
        raise NotImplementedError

    @classmethod
    async def delete_by_id(cls, async_session: AsyncSession, id: UUID):
        raise NotImplementedError

    @classmethod
    async def get_all(cls, async_session: AsyncSession):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, Generic[Model]):
    model: Model = None

    @classmethod
    async def get_by_id(
        cls,
        async_session: AsyncSession,
        id: UUID
    ) -> Model | None:
        logger.info({
            'action': 'SQLAlchemyRepository/get_by_id',
            'stage': 'start',
            'data': {'id': id}
        })
        async with async_session() as session:
            stmt = select(cls.model).where(cls.model.id == id)
            if hasattr(cls.model, "is_active"):
                stmt = stmt.where(cls.model.is_active)
            result = await session.scalar(stmt)
            logger.info({
                'action': 'SQLAlchemyRepository/get_by_id',
                'stage': 'end',
                'data': {'result': result}
            })
            return result

    @classmethod
    async def create(cls, async_session: AsyncSession, data: dict) -> Model:
        logger.info({
            'action': 'SQLAlchemyRepository/create',
            'stage': 'start',
            'data': {'data': data}
        })
        if not isinstance(data, dict):
            data = data.model_dump()
        async with async_session() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model)
            obj = await session.scalar(stmt)
            await session.commit()
            logger.info({
                'action': 'SQLAlchemyRepository/create',
                'stage': 'end',
                'data': {'created_obj': obj}
            })
            return obj

    @classmethod
    async def update_by_id(
        cls, async_session: AsyncSession, id: UUID, data: dict
    ) -> Model | None:
        logger.info({
            'action': 'SQLAlchemyRepository/update_by_id',
            'stage': 'start',
            'data': {'id': id, 'data': data}
        })
        if not isinstance(data, dict):
            data = data.model_dump()
        async with async_session() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(**data)
                .returning(cls.model)
            )
            obj = await session.scalar(stmt)
            await session.commit()
            logger.info({
                'action': 'SQLAlchemyRepository/update_by_id',
                'stage': 'end',
                'data': {'updated_obj': obj}
            })
            return obj

    @classmethod
    async def delete_by_id(
        cls,
        async_session: AsyncSession,
        id: UUID
    ) -> Model:
        logger.info({
            'action': 'SQLAlchemyRepository/delete_by_id',
            'stage': 'start',
            'data': {'id': id}
        })
        async with async_session() as session:
            stmt = delete(cls.model).where(
                cls.model.id == id
            ).returning(cls.model.id)

            obj = await session.scalar(stmt)
            await session.commit()
            logger.info({
                'action': 'SQLAlchemyRepository/delete_by_id',
                'stage': 'end',
                'data': {'deleted_id': obj}
            })
            return obj

    @classmethod
    async def get_all(cls, async_session: AsyncSession) -> list[Model] | None:
        logger.info({
            'action': 'SQLAlchemyRepository/get_all',
            'stage': 'start'
        })
        async with async_session() as session:
            stmt = select(cls.model)
            if hasattr(cls.model, "is_active"):
                stmt = stmt.where(cls.model.is_active)
            result = (await session.scalars(stmt)).all()
            logger.info({
                    'action': 'SQLAlchemyRepository/get_all',
                    'stage': 'end',
                    'data': {'result': result}
            })
            return result
