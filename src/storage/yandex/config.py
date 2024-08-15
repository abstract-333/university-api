from contextlib import asynccontextmanager

import yadisk

from settings import settings_obj


class YandexDiskConnectionFactory:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_instance()
        return cls._instance

    @classmethod
    @asynccontextmanager
    async def _create_instance(cls):
        async with yadisk.AsyncClient(
            token=settings_obj.YANDEX_API, session="httpx"
        ) as session:
            yield session
