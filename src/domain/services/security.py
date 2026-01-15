from typing import Any, Dict, Tuple

import jwt
from pydantic import ValidationError

from config import current_ts, settings
from domain.exceptions import UnauthorizedError

from ..enums import TokenType

MILLISECONDS_IN_DAY = 24 * 60 * 60 * 1000


def create_token(sub: Dict, token_type: TokenType, expire_days: int) -> Tuple[str, int]:
    expires_at = current_ts() + (expire_days * MILLISECONDS_IN_DAY)

    return (
        jwt.encode(
            {
                "sub": sub,
                "type": token_type,
                "exp": expires_at,
            },
            settings.secret_key.get_secret_value(),
            algorithm=settings.encrypt_algorithm,
        ),
        expires_at,
    )


def verify_token(token: str) -> Dict:
    return jwt.decode(
        token,
        settings.secret_key.get_secret_value(),
        algorithms=[settings.encrypt_algorithm],
    )


def validate_token(
    token: str, verify_exp: bool = True, token_type: TokenType = TokenType.access_token
) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=settings.encrypt_algorithm,
            options={"verify_exp": False},
        )

        if verify_exp and _token_is_expired(payload.get("exp")):
            raise UnauthorizedError.token_expired(
                token_type=payload.get("type"),
            )

        if payload.get("sub") is None:
            raise UnauthorizedError.invalid_token(
                token_type=payload.get("type"),
            )

        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError.token_expired(
            token_type=payload.get("type"),
        )
    except (jwt.PyJWTError, ValidationError):
        raise UnauthorizedError.invalid_token(
            token_type=token_type,
        )


def _token_is_expired(expired_at: int) -> bool:
    return expired_at < current_ts()
