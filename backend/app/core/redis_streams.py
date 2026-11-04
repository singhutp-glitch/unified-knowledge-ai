from redis.asyncio import Redis
from redis.exceptions import ResponseError


# Redis Stream name
STREAM_NAME = "sync:jobs"

# Consumer group name
GROUP_NAME = "sync-workers"


async def ensure_consumer_group(redis: Redis) -> None:

    try:
        await redis.xgroup_create(
            STREAM_NAME,
            GROUP_NAME,
            id="0-0",
            mkstream=True
        )

        print("Redis consumer group created successfully")

    except ResponseError as error:

        if "BUSYGROUP" in str(error):
            print("Redis consumer group already exists")

        else:
            raise