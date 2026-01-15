from sqlalchemy import Select, select

from dal.interfaces import IOneFetcher
from domain.models.users import User


class GetUserByEmailFetcher(IOneFetcher[User]):
    def _build_query(self, email: str) -> Select:
        return select(User).where(User.email == email)
