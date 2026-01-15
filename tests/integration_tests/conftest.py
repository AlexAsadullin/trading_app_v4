import pytest_asyncio
from httpx import ASGITransport

from config import settings
from domain.enums import TokenType
from domain.services import security
from tests.integration_tests.plugins import AsyncAppClient


@pytest_asyncio.fixture()
async def simple_api_client(app):
    transport = ASGITransport(app=app)
    async with AsyncAppClient(
        base_url="http://localhost:8000", transport=transport
    ) as client:
        yield client


@pytest_asyncio.fixture()
async def api_client(app, access_token, refresh_token):
    async with AsyncAppClient(
        base_url="http://localhost:8000", transport=ASGITransport(app=app)
    ) as client:
        client.headers["Authorization"] = f"Bearer {access_token}"
        client.cookies = {
            "refresh_token": refresh_token,
        }

        yield client


@pytest_asyncio.fixture()
async def access_token(user):
    token, _ = security.create_token(
        sub={
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
        token_type=TokenType.access_token,
        expire_days=settings.access_token_expire_days,
    )

    return token


@pytest_asyncio.fixture()
async def refresh_token(user):
    token, _ = security.create_token(
        sub={
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
        token_type=TokenType.refresh_token,
        expire_days=settings.refresh_token_expire_days,
    )
    return token
