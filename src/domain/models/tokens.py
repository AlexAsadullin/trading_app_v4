from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String

from config import current_ts
from domain.models.base import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    platform = Column(String, nullable=False)
    name = Column(String, nullable=False)
    token_encrypted = Column(String, nullable=False)
    date_added = Column(BigInteger, nullable=False, default=current_ts)
    expires_at = Column(BigInteger, nullable=False)
