from app.services import db_services
import time

def process_sync_job(sync_job_id: int):

     # 1. Retrieve the job and its associated changes
    job = db_services.get_sync_job_for_processing(
        sync_job_id
    )

    if not job:
        raise ValueError(
            f"Sync job {sync_job_id} not found"
        )

    print(f"Processing Sync Job: {sync_job_id}")

    # 2. Retrieve source information and credentials
    source = db_services.get_source_by_id(
        job["source_id"]
    )

    credentials = db_services.get_source_credentials_by_source_id(
        job["source_id"]
    )

    # 3. Process individual changes
    for change in job["changes"]:

        # Skip changes already successfully processed
        if change["status"] == "completed":
            continue

        print(
            f"Processing {change['file_name']}: "
            f"{change['change_type']}"
        )
        try:
            # Mark document as processing
            db_services.update_sync_job_change_status(
                change["id"],
                "processing"
            )

            # Dispatch according to change type
            if change["change_type"] == "added":

                add_company_document(
                    change,
                    credentials
                )

            elif change["change_type"] == "updated":

                update_company_document(
                    change,
                    credentials
                )

            elif change["change_type"] == "removed":

                remove_company_document(change)

            else:
                raise ValueError(
                    f"Unknown change type: {change['change_type']}"
                )

            # If the function returns without an exception,
            # consider the operation successful.
            db_services.update_sync_job_change_status(
                change["id"],
                "completed"
            )

        except Exception as error:

            logger.exception(
                "Failed to process document: %s",
                change["external_file_id"]
            )

            db_services.update_sync_job_change_status(
                change["id"],
                "failed",
                str(error)
            )

            # Continue processing the remaining documents
            continue

    # 4. Finalize overall job status
    final_status = db_services.finalize_sync_job(
    sync_job_id
    )

    print(
        f"Sync job {sync_job_id} final status: {final_status}"
    )