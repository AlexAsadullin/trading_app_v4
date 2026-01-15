from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings


def get_async_engine():
    return create_async_engine(
        str(settings.db_dsn),
        echo=settings.db_echo,
        connect_args={
            "server_settings": {"jit": "off", "options": f"-c timezone={settings.tz}"}
        },
        pool_use_lifo=True,
        pool_recycle=3600,
    )


@asynccontextmanager
async def create_session_factory():
    session_factory = async_sessionmaker(get_async_engine())
    async with session_factory() as session:
        yield session
