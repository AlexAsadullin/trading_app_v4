from sqlalchemy import BigInteger, Column, text
from sqlalchemy.orm import DeclarativeBase

from config import current_ts


class Base(DeclarativeBase):
    pass


class HistoricalMixin:
    created_timestamp = Column(
        BigInteger,
        nullable=False,
        server_default=text("EXTRACT(EPOCH FROM NOW()) * 1000"),
        default=current_ts,
    )


class TimestampMixin:
    created_at = Column(
        BigInteger,
        nullable=False,
        server_default=text("EXTRACT(EPOCH FROM NOW()) * 1000"),
        default=current_ts(),
    )
    updated_at = Column(
        BigInteger,
        nullable=False,
        server_default=text("EXTRACT(EPOCH FROM NOW()) * 1000"),
        onupdate=current_ts(),
    )
    deleted_at = Column(BigInteger, nullable=True)
