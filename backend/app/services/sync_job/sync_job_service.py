from fastapi import HTTPException
from redis.exceptions import RedisError

from app.core.redis_client import redis_client
from app.core.redis_streams import STREAM_NAME
from app.services import db_services
from sqlalchemy.exc import IntegrityError

async def create_sync_job_and_enqueue(
    source_id,
    user_id,
    changes_to_sync
):
    # 1. Create parent job and child records in PostgreSQL
    # This operation commits everything in one transaction.

    try:
        sync_job_id = db_services.create_sync_job_with_changes(
            source_id=source_id,
            user_id=user_id,
            changes=changes_to_sync
        )

    except IntegrityError:
        # Another request may have created the active job first.
        active_job = db_services.get_active_sync_job(source_id)

        if active_job:
            return {
                "sync_job_id": active_job.id,
                "status": active_job.status,
                "message": "A synchronization job is already active."
            }

        raise

    # 2. Publish the job ID to Redis
    try:
        redis_message_id = await redis_client.xadd(
            STREAM_NAME,
            {
                "job_id": str(sync_job_id)
            }
        )

    except RedisError as error:

        # The PostgreSQL job still exists.
        # Record the dispatch failure for later recovery.
        db_services.update_sync_job_dispatch_error(
            sync_job_id,
            str(error)
        )

        raise HTTPException(
            status_code=503,
            detail={
                "message": "Sync job was saved but could not be added to the processing queue.",
                "sync_job_id": sync_job_id
            }
        )

    # 3. Record successful Redis dispatch
    db_services.mark_sync_job_enqueued(
        sync_job_id,
        redis_message_id
    )

    # 4. Return job information
    return {
        "sync_job_id": sync_job_id,
        "status": "queued",
        "total_files": len(changes_to_sync)
    }