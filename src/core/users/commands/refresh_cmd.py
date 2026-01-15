from typing import Dict

from config import settings
from domain.enums import TokenType
from domain.exceptions import UnauthorizedError
from domain.services import security

from ..dtos import RefreshTokenDto, TokenData
from ..mixins import GetUserMixin


class RefreshTokenCommand(GetUserMixin):
    async def execute(self, refresh_token: str) -> RefreshTokenDto:
        payload = self.__validate_refresh_token(refresh_token)

        email = payload.get("email")
        user = await self.get_user(email=email)
        if not user:
            raise UnauthorizedError.invalid_token(
                token_type=TokenType.refresh_token,
            )

        sub = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }
        access_token_data = self.__create_tokens(
            sub=sub,
            token_type=TokenType.access_token,
            expire_days=settings.access_token_expire_days,
        )
        refresh_token_data = self.__create_tokens(
            sub=sub,
            token_type=TokenType.refresh_token,
            expire_days=settings.refresh_token_expire_days,
        )

        return RefreshTokenDto(
            access_token=access_token_data,
            refresh_token=refresh_token_data,
        )

    def __create_tokens(
        self, sub: Dict, token_type: TokenType, expire_days: int
    ) -> TokenData:
        token, expired_at = security.create_token(
            sub=sub,
            token_type=token_type,
            expire_days=expire_days,
        )
        return TokenData(token=token, expired_at=expired_at)

    def __validate_refresh_token(self, refresh_token: str) -> Dict:
        payload = security.validate_token(
            refresh_token, token_type=TokenType.refresh_token
        )

        if payload.get("type") != TokenType.refresh_token:
            raise UnauthorizedError.invalid_token(
                token_type=TokenType.refresh_token,
            )

        return payload.get("sub")
