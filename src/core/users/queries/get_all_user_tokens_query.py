from dal.fetchers.tokens import GetAllUserTokensFetcher
from domain.services.encryption import decrypt_token

from ..dtos import ApiTokenListItemDto


class GetAllUserTokensQuery:
    async def execute(self, user_id: int) -> list[ApiTokenListItemDto]:
        fetcher = GetAllUserTokensFetcher()
        tokens = await fetcher.fetch(user_id=user_id)

        return [
            ApiTokenListItemDto(
                id=token.id,
                platform=token.platform,
                name=token.name,
                date_added=token.date_added,
                expires_at=token.expires_at,
            )
            for token in tokens
        ]
