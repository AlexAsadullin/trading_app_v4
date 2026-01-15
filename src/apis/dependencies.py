from typing import Any, Dict

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.users.dtos import UserProfile
from dal.fetchers.users import GetUserByEmailFetcher
from domain.enums import TokenType
from domain.exceptions import UnauthorizedError
from domain.services.security import validate_token

TokenPayload = Dict[str, Any]


class TokenValidator(HTTPBearer):
    def __init__(self) -> None:
        super().__init__(auto_error=False)

    async def __call__(self, request: Request) -> TokenPayload | None:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(
            request
        )
        if not credentials:
            return None

        return validate_token(credentials.credentials)


async def get_current_user(
    token_payload: TokenPayload | None = Depends(TokenValidator()),
) -> UserProfile:
    if not token_payload:
        raise UnauthorizedError.invalid_token(token_type=TokenType.access_token)

    user_data = token_payload.get("sub")
    if not user_data or not user_data.get("email"):
        raise UnauthorizedError.invalid_token(token_type=TokenType.access_token)

    user = await GetUserByEmailFetcher().fetch(email=user_data.get("email"))
    if not user:
        raise UnauthorizedError.invalid_token(token_type=TokenType.access_token)

    return UserProfile.model_validate(user)
