from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from app.constants import GOOGLE_DRIVE_SCOPE
from app.services import db_services
from app.config import settings

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

