import datetime
import uuid

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


class TimeStampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
    )
