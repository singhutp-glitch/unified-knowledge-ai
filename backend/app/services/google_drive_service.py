from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from app.constants import GOOGLE_DRIVE_SCOPE
from app.services import db_services
from app.config import settings

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"

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