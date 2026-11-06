from app.services import db_services


def process_sync_job(sync_job_id: int):

    print(f"Starting test processing for job {sync_job_id}")

    # Simulate successful processing of all documents
    db_services.mark_sync_job_successful_for_testing(
        sync_job_id
    )

    print(f"Sync job {sync_job_id} completed successfully")

    return True