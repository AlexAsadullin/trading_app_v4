from dal.fetchers.users import GetUserByEmailFetcher
from domain.exceptions import NotFoundError
from domain.models.users import User


class GetUserOrRaiseMixin:
    async def get_user_or_raise(self, email: str) -> User:
        user = await GetUserByEmailFetcher().fetch(email=email)
        if not user:
            raise NotFoundError(entity_name="User", entity_id=email)

        return user


class GetUserMixin:
    async def get_user(self, email: str) -> User | None:
        return await GetUserByEmailFetcher().fetch(email=email)
