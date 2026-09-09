from google_auth_oauthlib.flow import Flow

from app.config import settings


GOOGLE_DRIVE_SCOPE = [
    "https://www.googleapis.com/auth/drive.readonly"
]


def create_authorization_url():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.google_redirect_uri],
            }
        },
        scopes=GOOGLE_DRIVE_SCOPE,
    )

    flow.redirect_uri = settings.google_redirect_uri

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    return authorization_url, state


def exchange_code_for_credentials(code: str, state: str):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.google_redirect_uri],
            }
        },
        scopes=GOOGLE_DRIVE_SCOPE,
        state=state,
    )

    flow.redirect_uri = settings.google_redirect_uri

    flow.fetch_token(code=code)

    return flow.credentials