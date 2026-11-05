def process_sync_job(sync_job_id: int):

    # 1. Fetch the SyncJob from PostgreSQL.

    # 2. Fetch its SyncJobChange records.

    # 3. Process each document:
    #       - Mark the change as processing.
    #       - Download from Google Drive.
    #       - Extract document content.
    #       - Chunk the content.
    #       - Generate embeddings.
    #       - Store/update the document.
    #       - Mark the change completed or failed.

    # 4. Recalculate parent job progress.

    # 5. Set the final job status:
    #       completed
    #       completed_with_errors
    #       failed

    # 6. Clear locked_by and locked_until.

    pass