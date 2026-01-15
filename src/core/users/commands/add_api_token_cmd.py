from fastapi_async_sqlalchemy import db

from config import current_ts
from domain.models.tokens import Token
from domain.services.encryption import encrypt_token

from ..dtos import ApiTokenDto


class AddApiTokenCommand:
    async def execute(
        self, user_id: int, platform: str, name: str, token: str, expires_at: int
    ) -> ApiTokenDto:
        token_encrypted = encrypt_token(token)

        api_token = Token()
        api_token.user_id = user_id
        api_token.platform = platform
        api_token.name = name
        api_token.token_encrypted = token_encrypted
        api_token.date_added = current_ts()
        api_token.expires_at = expires_at

        db.session.add(api_token)
        await db.session.commit()
        await db.session.refresh(api_token)

        return ApiTokenDto(
            id=api_token.id,
            user_id=api_token.user_id,
            platform=api_token.platform,
            name=api_token.name,
            date_added=api_token.date_added,
            expires_at=api_token.expires_at,
        )
