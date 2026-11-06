import redis
from app.config import settings


def create_sync_redis_client():

    return redis.Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=10,
        socket_timeout=15
    )

# Application-owned Redis client
redis_client = create_sync_redis_client()