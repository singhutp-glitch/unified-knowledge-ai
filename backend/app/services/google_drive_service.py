import io

from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from app.constants import GOOGLE_DRIVE_SCOPE
from app.services import db_services
from app.config import settings

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"


GOOGLE_EXPORT_TYPES = {
    "application/vnd.google-apps.document":
        "application/pdf",

    "application/vnd.google-apps.spreadsheet":
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

    "application/vnd.google-apps.presentation":
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}

def get_valid_access_token(credentials_row):

    credentials = Credentials(
        token=credentials_row.access_token,
        refresh_token=credentials_row.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        scopes=GOOGLE_DRIVE_SCOPE,
    )

    if not credentials.valid:
        credentials.refresh(Request())
        update_access_token(
            credentials_row.source_id,
            credentials.token,
            credentials.expiry
        )

    return credentials.token


def get_folder(credentials, folder_id):

    access_token = get_valid_access_token(credentials)

    google_credentials = Credentials(
        token=access_token,
        refresh_token=credentials.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        scopes=GOOGLE_DRIVE_SCOPE,
    )

    drive_service = build(
        "drive",
        "v3",
        credentials=google_credentials
    )

    folder = drive_service.files().get(
        fileId=folder_id,
        fields="id,name,mimeType"
    ).execute()

    return folder



def list_files_in_root_folder(credentials_row, root_folder_id):

    access_token = get_valid_access_token(credentials_row)

    google_credentials = Credentials(
        token=access_token,
        refresh_token=credentials_row.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        scopes=GOOGLE_DRIVE_SCOPE,
    )

    drive_service = build(
        "drive",
        "v3",
        credentials=google_credentials
    )

    files = []
    folders_to_visit = [root_folder_id]

    while folders_to_visit:

        current_folder_id = folders_to_visit.pop()
        page_token = None

        while True:

            response = drive_service.files().list(
                q=(
                    f"'{current_folder_id}' in parents "
                    "and trashed = false"
                ),
                fields=(
                    "nextPageToken,"
                    "files("
                    "id,"
                    "name,"
                    "mimeType,"
                    "modifiedTime,"
                    "size"
                    ")"
                ),
                pageSize=1000,
                pageToken=page_token
            ).execute()

            for file in response.get("files", []):

                if file["mimeType"] == FOLDER_MIME_TYPE:
                    folders_to_visit.append(file["id"])
                else:
                    files.append(file)

            page_token = response.get("nextPageToken")

            if not page_token:
                break

    return files


def download_drive_file(credentials, file_id):

    access_token = get_valid_access_token(credentials)

    google_credentials = Credentials(
        token=access_token,
        refresh_token=credentials.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        scopes=GOOGLE_DRIVE_SCOPE,
    )

    drive_service = build(
        "drive",
        "v3",
        credentials=google_credentials
    )

    # 1. Retrieve file metadata
    metadata = drive_service.files().get(
        fileId=file_id,
        fields="id,name,mimeType,size,modifiedTime,capabilities(canDownload)"
    ).execute()

    mime_type = metadata["mimeType"]
    modified_time = metadata["modifiedTime"]

    # 2. Check download permissions
    if metadata.get("capabilities", {}).get("canDownload") is False:
        raise PermissionError(
            f"Cannot download Google Drive file: {metadata['name']}"
        )

    # 3. Handle native Google Workspace documents
    if mime_type in GOOGLE_EXPORT_TYPES:

        export_mime_type = GOOGLE_EXPORT_TYPES[mime_type]

        content = drive_service.files().export(
            fileId=file_id,
            mimeType=export_mime_type
        ).execute()

    # 4. Handle ordinary uploaded files
    else:

        request = drive_service.files().get_media(
            fileId=file_id
        )

        file_buffer = io.BytesIO()

        downloader = MediaIoBaseDownload(
            file_buffer,
            request
        )

        done = False

        while not done:
            status, done = downloader.next_chunk()

        content = file_buffer.getvalue()

        export_mime_type = mime_type

    # 5. Return file information and its contents
    return {
        "file_id": metadata["id"],
        "file_name": metadata["name"],
        "mime_type": mime_type,
        "downloaded_mime_type": export_mime_type,
        "content": content,
        "modified_time": modified_time
    }