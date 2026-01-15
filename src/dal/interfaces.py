from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Generic, List, TypeVar

from fastapi_async_sqlalchemy import db
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class IOneFetcher(ABC, Generic[T]):
    def __init__(self) -> None:
        self.session: AsyncSession = db.session

    @abstractmethod
    def _build_query(self, *args: Any, **kwargs: Any) -> Select:
        raise NotImplementedError

    async def fetch(self, *args: Any, **kwargs: Any) -> T | None:
        query = self._build_query(*args, **kwargs)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()


class IManyFetcher(Generic[T], metaclass=ABCMeta):
    db_session = None

    def __init__(
        self, db_session: AsyncSession | None = None, fetch_one: bool = False
    ) -> None:
        self.db_session = db_session
        self.fetch_one = fetch_one

        return None

    async def fetch(self, *args, **kwargs) -> List[T]:
        query = self._build_query(*args, **kwargs)

        if self.db_session is not None:
            result = await self.db_session.execute(query)
        else:
            result = await db.session.execute(query)

        return result.scalars().all()

    @abstractmethod
    def _build_query(self, *args, **kwargs) -> T:
        raise NotImplementedError
