from functools import lru_cache

from redis.asyncio import Redis

from settings.settings import get_settings


@lru_cache
def get_redis_client():
    s = get_settings().REDIS
    redis_client = Redis(host=s.HOST, port=s.PORT, db=s.DB, decode_responses=True)
    return redis_client
