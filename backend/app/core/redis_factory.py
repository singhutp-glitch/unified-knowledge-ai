import redis
from redis.asyncio import Redis as AsyncRedis

from app.config import settings


# For the primary FastAPI application
def create_sync_redis_client():

    return redis.Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=10,
        socket_timeout=15
    )


# For the Redis consumer
def create_async_redis_client():

    return AsyncRedis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=10,
        socket_timeout=30
    )