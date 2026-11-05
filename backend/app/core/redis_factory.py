from redis.asyncio import Redis
from app.config import settings


def create_redis_client() -> Redis:

    return Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=10,
        socket_timeout=30,
        health_check_interval=30
    )