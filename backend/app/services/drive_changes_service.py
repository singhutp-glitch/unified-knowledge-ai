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
        document.external_file_id: document
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

        if document.external_modified_at is None:
            updated.append({
                "type": "updated",
                "file": drive_file
            })

            continue

        # If your DB stores naive UTC datetimes,
        # normalize here before comparison.
        if drive_modified_at != document.external_modified_at:
            updated.append({
                "type": "updated",
                "file": drive_file
            })

        elif document.name != drive_file["name"]:
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
                    "id": document.external_file_id,
                    "name": document.name
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