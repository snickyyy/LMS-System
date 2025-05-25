from functools import lru_cache

from redis.asyncio import Redis

from api.interfaces.redis_repository import IBaseRedisRepository
from settings.redis import get_redis_client


class BaseRedisRepository(IBaseRedisRepository):
    _client = get_redis_client()

    async def set(self, prefix: str, key: str, value: str, exat: int = 0):
        result = await self._client.set(f"{prefix}:{key}", value, exat=exat)
        return result

    async def get(self, prefix: str, key: str):
        result = await self._client.get(f"{prefix}:{key}")
        return result

    async def delete(self, prefix: str, key: str):
        result = await self._client.delete(f"{prefix}:{key}")
        return result

    async def exists(self, prefix: str, key: str):
        result = await self._client.exists(f"{prefix}:{key}")
        return result

    async def count(self):
        result = await self._client.dbsize()
        return result

@lru_cache
def get_redis_repository() -> BaseRedisRepository:
    return BaseRedisRepository()
