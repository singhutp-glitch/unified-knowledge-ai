
from googleapiclient.discovery import build

from app.sources.google_drive.oauth import exchange_code_for_credentials
from app.services import db_service
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from app.sources.google_drive.oauth import create_authorization_url
from app.source.google_drive.oauth_state import oauth_states

def connect_google_drive(user_id: int):

    authorization_url, state = create_authorization_url()

    oauth_states[state] = user_id

    return RedirectResponse(authorization_url)



def google_drive_callback(code: str, state: str):

    # --------------------------------------------------
    # 1. Verify OAuth state
    # --------------------------------------------------

    user_id = oauth_states.pop(state, None)

    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OAuth state"
        )

    # --------------------------------------------------
    # 2. Exchange authorization code for credentials
    # --------------------------------------------------

    try:
        credentials = exchange_code_for_credentials(code, state)

    except Exception as error:
        print(f"Google OAuth token exchange failed: {error}")

        raise HTTPException(
            status_code=400,
            detail="Failed to complete Google authorization"
        )

    # --------------------------------------------------
    # 3. Get the Google account email
    # --------------------------------------------------

    try:
        drive_service = build(
            "drive",
            "v3",
            credentials=credentials
        )

        about = drive_service.about().get(
            fields="user(emailAddress)"
        ).execute()

        account_email = about["user"]["emailAddress"]

    except Exception as error:
        print(f"Failed to get Google account information: {error}")

        raise HTTPException(
            status_code=400,
            detail="Failed to retrieve Google account information"
        )

    # --------------------------------------------------
    # 4. Check whether Google Drive is already connected
    # --------------------------------------------------

    existing_source = db_service.get_source_by_type(
        "google_drive"
    )

    # --------------------------------------------------
    # 5. Create or update source
    # --------------------------------------------------

    try:

        if existing_source:

            source = db_service.update_source(
                source_id=existing_source.id,
                status="connected",
                account_email=account_email
            )

        else:

            source = db_service.create_source(
                type="google_drive",
                name="Google Drive",
                status="connected",
                account_email=account_email
            )

        # --------------------------------------------------
        # 6. Save OAuth credentials
        # --------------------------------------------------

        existing_credentials = (
            db_service.get_credentials_by_source_id(
                source.id
            )
        )

        if existing_credentials:

            db_service.update_credentials(
                source_id=source.id,
                access_token=credentials.token,
                refresh_token=(
                    credentials.refresh_token
                    or existing_credentials.refresh_token
                ),
                token_expiry=credentials.expiry
            )

        else:

            db_service.create_credentials(
                source_id=source.id,
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                token_expiry=credentials.expiry
            )

    except Exception as error:
        print(f"Failed to save Google Drive connection: {error}")

        raise HTTPException(
            status_code=500,
            detail="Failed to save Google Drive connection"
        )

    # --------------------------------------------------
    # 7. Redirect admin back to frontend
    # --------------------------------------------------

    return RedirectResponse(
        url=(
            f"http://localhost:5173/"
            f"company-knowledge/sources/{source.id}/enrollment"
        )
    )