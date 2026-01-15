import pytest_asyncio

from config import current_ts, settings
from domain.enums import TokenType
from domain.services import security


@pytest_asyncio.fixture()
async def access_token_expired_at():
    return current_ts() + (settings.access_token_expire_days * 24 * 60 * 60 * 1000)


@pytest_asyncio.fixture()
async def login_request_body(user):
    return {
        "email": user.email,
        "password": "test",
    }


@pytest_asyncio.fixture()
async def invalid_refresh_token_creator():

    def create(existing_refresh_token, expire_days, email):
        if not existing_refresh_token:
            if not email:
                return None
            token, _ = security.create_token(
                sub={
                    "email": email,
                },
                token_type=TokenType.refresh_token,
                expire_days=expire_days,
            )
            return token
        return existing_refresh_token

    return create


@pytest_asyncio.fixture()
async def register_request_body():
    return {
        "email": "test+1@test.com",
        "password": "test",
        "name": "test",
    }


@pytest_asyncio.fixture()
async def register_request_body_with_existing_email(user):
    return {
        "email": user.email,
        "password": "test",
        "name": "test",
    }


@pytest_asyncio.fixture()
async def register_request_body_with_invalid_email():
    return {
        "email": "invalid-email",
        "password": "test",
        "name": "test",
    }
