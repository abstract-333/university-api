from redis import asyncio as aioredis, Redis
from settings import settings_obj


class RedisConnectionFactory:
    _instance = None

    @classmethod
    async def get_instance(cls) -> Redis:
        if cls._instance is None:
            cls._instance = await cls._create_instance()
        return cls._instance

    @classmethod
    async def _create_instance(cls) -> Redis:
        redis = await aioredis.from_url(
            url=f"redis://{settings_obj.REDIS_HOST}:{settings_obj.REDIS_PORT}",
            encoding="utf8",
            decode_responses=True,
        )
        return redis
