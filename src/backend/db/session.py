from typing import Callable

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.backend.config import config


class SessionManager:
    """Класс, предоставляющий сессии для проекта."""

    def __init__(self, db_dsn: str, echo: bool = False):
        self.engine = create_async_engine(
            url=db_dsn,
            echo=echo,
        )

    @property
    def async_session(self) -> Callable[..., AsyncSession]:
        return self.create_session_factory()

    def create_session_factory(self) -> Callable[..., AsyncSession]:
        return async_sessionmaker(
            self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )


session_manager = SessionManager(
    db_dsn=config.postgres.get_dsn,
    echo=config.app.debug,
)
