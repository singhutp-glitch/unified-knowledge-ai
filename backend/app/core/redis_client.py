from redis.asyncio import Redis
from app.config import settings


def create_redis_client() -> Redis:
    return Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )


# Application-owned Redis client
redis_client = create_redis_client()