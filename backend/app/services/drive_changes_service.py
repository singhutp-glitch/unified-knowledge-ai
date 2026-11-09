from datetime import datetime


def parse_drive_datetime(value: str) -> datetime:
    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )


def calculate_changes(drive_files, company_documents):

    drive_by_id = {
        file["id"]: file
        for file in drive_files
    }

    document_by_id = {
        document.company_details.external_file_id: document
        for document in company_documents
    }

    added = []
    updated = []
    removed = []

    # Detect added and updated files
    for file_id, drive_file in drive_by_id.items():

        document = document_by_id.get(file_id)

        if document is None:

            added.append({
                "type": "added",
                "file": drive_file
            })

            continue

        drive_modified_at = parse_drive_datetime(
            drive_file["modifiedTime"]
        )

        if document.company_details.external_modified_at is None:
            updated.append({
                "type": "updated",
                "file": drive_file
            })

            continue

        # If your DB stores naive UTC datetimes,
        # normalize here before comparison.
        if drive_modified_at != document.company_details.external_modified_at:
            updated.append({
                "type": "updated",
                "file": drive_file
            })

        elif document.original_file_name != drive_file["name"]:
            updated.append({
                "type": "updated",
                "file": drive_file
            })

    # Detect removed files
    for external_file_id, document in document_by_id.items():

        if external_file_id not in drive_by_id:

            removed.append({
                "type": "removed",
                "file": {
                    "id": document.company_details.external_file_id,
                    "name": document.original_file_name
                }
            })

    return {
        "summary": {
            "added": len(added),
            "updated": len(updated),
            "removed": len(removed),
            "total": len(added) + len(updated) + len(removed)
        },
        "changes": added + updated + removed
    }


def validate_changes(sync_changes: list[str], changes: dict) -> dict:

    # Get the actual changes calculated by the backend
    current_changes = changes.get("changes", [])

    # Create a lookup using Google Drive file IDs
    changes_by_id = {
        change["file"]["id"]: change
        for change in current_changes
    }

    valid_changes = []
    invalid_ids = []
    duplicate_ids = []
    seen_ids = set()

    # Validate every ID received from the frontend
    for file_id in sync_changes:

        # Check for duplicate IDs
        print("file_id: ",file_id)
        if file_id in seen_ids:
            duplicate_ids.append(file_id)
            continue

        seen_ids.add(file_id)

        # Check whether the ID represents an actual change
        change = changes_by_id.get(file_id)

        if change is None:
            invalid_ids.append(file_id)
        else:
            valid_changes.append(change)

    is_valid = (
        len(sync_changes) > 0
        and len(invalid_ids) == 0
        and len(duplicate_ids) == 0
    )

    return {
        "is_valid": is_valid,
        "changes_to_sync": valid_changes if is_valid else [],
        "invalid_ids": invalid_ids,
        "duplicate_ids": duplicate_ids
    }