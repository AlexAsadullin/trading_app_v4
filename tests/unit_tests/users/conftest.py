import pytest_asyncio

from config import current_ts, settings
from core.users.dtos import TokenData
from domain.enums import TokenType
from domain.services import security


@pytest_asyncio.fixture()
async def sub_data(user):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
    }


@pytest_asyncio.fixture()
async def refresh_token_data(sub_data, db_sessions):
    token, expired_at = security.create_token(
        sub=sub_data,
        token_type=TokenType.refresh_token,
        expire_days=settings.refresh_token_expire_days,
    )

    return TokenData(token=token, expired_at=expired_at)


@pytest_asyncio.fixture()
async def expired_refresh_token_data(sub_data, db_sessions):
    expired_at = current_ts() - 1

    token, expired_at = security.create_token(
        sub=sub_data,
        token_type=TokenType.refresh_token,
        expire_days=-1,
    )
    return TokenData(token=token, expired_at=expired_at)
