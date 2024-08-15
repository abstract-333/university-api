from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from settings import settings_obj


class AsyncSessionFactory:
    _instance = None
    _async_engine = None
    _async_session_maker = None

    @classmethod
    def get_instance(cls) -> async_sessionmaker[AsyncSession]:
        if cls._instance is None:
            cls._instance: async_sessionmaker[AsyncSession] = cls._create_instance()
        return cls._instance

    @classmethod
    def _create_instance(cls) -> async_sessionmaker[AsyncSession]:
        cls._async_engine: AsyncEngine = create_async_engine(
            url=settings_obj.database_url, echo=True, pool_size=20, max_overflow=0
        )
        cls._async_session_maker = async_sessionmaker(
            cls._async_engine, expire_on_commit=False
        )
        return cls._async_session_maker

    @staticmethod
    async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
        session_maker: async_sessionmaker[
            AsyncSession
        ] = AsyncSessionFactory.get_instance()
        async with session_maker() as session:
            yield session

    @classmethod
    def get_async_engine(cls) -> AsyncEngine:
        if cls._async_engine is None:
            cls.get_instance()
        return cls._async_engine

    @classmethod
    def get_async_session_maker(cls) -> async_sessionmaker[AsyncSession]:
        if cls._async_session_maker is None:
            cls.get_instance()
        return cls._async_session_maker
