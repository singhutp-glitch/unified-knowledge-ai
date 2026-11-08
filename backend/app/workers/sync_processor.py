from app.services import db_services
import time

async def process_sync_job(sync_job_id: int):

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
        if(change["change_type"]=="added"):
            await add_company_document(change,credentials)


        # Your document processing logic goes here

    # 4. Finalize the job