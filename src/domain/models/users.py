from passlib.context import CryptContext
from sqlalchemy import BigInteger, Column, Integer, String

from config import current_ts
from domain.models.base import Base

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Integer)
    phone_number = Column(String)
    register_date = Column(BigInteger, nullable=False, default=current_ts)

    def __init__(self, email: str, password: str, first_name: str, last_name: str, birth_date: int, phone_number: str) -> None:
        self.email = email
        self.password_hash = PASSWORD_CONTEXT.hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone_number = phone_number
        self.register_date = current_ts()

    def verify_password(self, password: str) -> bool:
        return PASSWORD_CONTEXT.verify(password, self.password_hash)
