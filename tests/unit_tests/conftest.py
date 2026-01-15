import uuid

import pytest_asyncio

from domain.models import User


@pytest_asyncio.fixture()
async def new_user(saver):
    user = User(email=f"new-user+{uuid.uuid4()}@test.com", password="test", name="test")
    return await saver(user)
