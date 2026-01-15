from dal.fetchers.tokens import GetTokenByIdFetcher
from domain.exceptions import NotFoundError
from fastapi_async_sqlalchemy import db


class DeleteApiTokenCommand:
    async def execute(self, token_id: int, user_id: int) -> None:
        token = await GetTokenByIdFetcher().fetch(token_id=token_id, user_id=user_id)
        if not token:
            raise NotFoundError(entity_name="Token", entity_id=token_id)

        await db.session.delete(token)
        await db.session.commit()
