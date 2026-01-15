import pytest_asyncio
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db
from pydantic import PostgresDsn
from testcontainers.postgres import PostgresContainer

from apis.create_app import create_app
from config import settings
from dal.engines import create_session_factory
from domain.models.base import Base
from domain.models.users import User


@pytest_asyncio.fixture(scope="session")
async def postgres_container():
    with PostgresContainer("postgres:17", driver="asyncpg").with_exposed_ports(
        5434
    ) as pg:
        settings.db_dsn = PostgresDsn(pg.get_connection_url())
        async with create_session_factory() as session:
            conn = await session.connection()
            await conn.run_sync(Base.metadata.create_all)
            await session.commit()
        yield pg


@pytest_asyncio.fixture()
async def app(postgres_container):
    app = create_app()

    yield app


@pytest_asyncio.fixture()
async def db_sessions(app):
    async with db() as session:
        yield session


@pytest_asyncio.fixture()
async def saver(db_sessions):
    async def save_entity(entity):
        db_sessions.session.add(entity)
        await db_sessions.session.commit()
        await db_sessions.session.refresh(entity)

        return entity

    return save_entity


@pytest_asyncio.fixture()
async def saver_many(db_sessions):
    async def save_entities(entities):
        db_sessions.session.add_all(entities)
        await db_sessions.session.commit()

        return entities

    return save_entities


@pytest_asyncio.fixture(scope="session")
async def user(postgres_container):
    user = User(email="test@test.com", password="test", name="test")
    async with create_session_factory() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user
