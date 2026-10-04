from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from app.constants import GOOGLE_DRIVE_SCOPE
from app.services import db_services

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