from app.core.redis_factory import create_redis_client
from app.core.redis_streams import ensure_consumer_group


async def run_consumer():

    redis = create_redis_client()

    try:
        # Create the Stream and consumer group if necessary
        await ensure_consumer_group(redis)

        print("Redis consumer initialized")

        # await consume_sync_jobs(redis)

    finally:
        await redis.aclose()