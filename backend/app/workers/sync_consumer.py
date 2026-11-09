from app.services import db_services
import asyncio
import logging
from app.core.redis_factory import create_async_redis_client
import uuid
from app.core.redis_streams import (
    STREAM_NAME,
    GROUP_NAME,
    ensure_consumer_group
)
from app.workers.sync_processor import process_sync_job
from redis.exceptions import RedisError
logger = logging.getLogger(__name__)

CONSUMER_NAME = f"sync-consumer-{uuid.uuid4().hex[:8]}"

TERMINAL_STATUSES = {
    "completed",
    "completed_with_errors",
    "failed",
    "cancelled"
}

PENDING_IDLE_MS = 60*60 * 1000  # 60 minutes


async def handle_sync_message(redis, message_id, fields):

    # 1. Extract the PostgreSQL job ID
    try:
        job_id = int(fields["job_id"])

    except (KeyError, ValueError):
        logger.error(
            "Invalid sync message: %s",
            fields
        )

        # Poison message: it cannot be processed.
        await redis.xack(
            STREAM_NAME,
            GROUP_NAME,
            message_id
        )
        return

    # 2. Atomically claim the job in PostgreSQL
    claim_result = await asyncio.to_thread(
        db_services.claim_sync_job,
        job_id,
        CONSUMER_NAME
    )

    if claim_result == "terminal":
        # Already completed or permanently failed.
        await redis.xack(STREAM_NAME, GROUP_NAME, message_id)
        return

    if claim_result == "not_found":
        logger.error("Sync job %s does not exist", job_id)
        await redis.xack(STREAM_NAME, GROUP_NAME, message_id)
        return

    if claim_result == "active":
        # Another execution still has a valid processing lease.
        # Leave this message pending.
        return

    if claim_result != "claimed":
        logger.error(
            "Unexpected claim result for job %s: %s",
            job_id,
            claim_result
        )
        return

    # 3. Execute the actual synchronization job
    try:
        await process_sync_job(job_id)
    
    except Exception:
        logger.exception(
            "Error processing sync job %s",
            job_id
        )

        # Do not acknowledge it.
        # It can be recovered later using XAUTOCLAIM.
        return

    # 4. Check whether processing reached a terminal state
    final_status = await asyncio.to_thread(
        db_services.get_sync_job_status,
        job_id
    )

    if final_status in TERMINAL_STATUSES:

        # 5. Acknowledge the Redis message
        await redis.xack(
            STREAM_NAME,
            GROUP_NAME,
            message_id
        )

        logger.info(
            "Sync job %s finished with status %s",
            job_id,
            final_status
        )

    else:
        logger.warning(
            "Sync job %s is not yet complete; leaving message pending",
            job_id
        )


async def consume_sync_jobs(redis):

    logger.info(
        "Redis consumer started: %s",
        CONSUMER_NAME
    )

    while True:

        try:
            await recover_pending_sync_jobs(redis)

            # Read new messages from the consumer group
            messages = await redis.xreadgroup(
                groupname=GROUP_NAME,
                consumername=CONSUMER_NAME,
                streams={
                    STREAM_NAME: ">"
                },
                count=1,
                block=5000
            )
            if not messages:
                continue

            for stream_name, entries in messages:

                for message_id, fields in entries:

                    await handle_sync_message(
                        redis,
                        message_id,
                        fields
                    )

        except asyncio.CancelledError:
            logger.info("Redis consumer shutting down")
            raise

        except RedisError:
            logger.exception(
                "Redis communication error"
            )

            await asyncio.sleep(3)

        except Exception:
            logger.exception(
                "Unexpected consumer error"
            )

            await asyncio.sleep(3)


async def recover_pending_sync_jobs(redis):

    result = await redis.xautoclaim(
        name=STREAM_NAME,
        groupname=GROUP_NAME,
        consumername=CONSUMER_NAME,
        min_idle_time=PENDING_IDLE_MS,
        start_id="0-0",
        count=1
    )

    # redis-py returns:
    # (next_start_id, messages, deleted_ids)
    next_start_id, claimed_messages = result[:2]

    deleted_ids = result[2] if len(result) > 2 else []

    for deleted_id in deleted_ids:
        logger.error(
            "Pending Redis message %s no longer exists in the stream",
            deleted_id
        )

    for message_id, fields in claimed_messages:

        logger.info(
            "Recovering pending sync message %s",
            message_id
        )

        await handle_sync_message(
            redis,
            message_id,
            fields
        )

    
async def run_consumer():

    redis = create_async_redis_client()

    try:
        # Ensure the stream and consumer group exist
        await ensure_consumer_group(redis)

        logger.info("Sync consumer initialized")

        # Start continuously reading jobs
        await consume_sync_jobs(redis)

    finally:
        # Close the consumer's own Redis connection
        await redis.aclose()