from app.sources.google_drive.oauth import revoke_google_credentials
from googleapiclient.discovery import build

from app.sources.google_drive.oauth import exchange_code_for_credentials
from app.services import db_services, google_drive_service
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from app.sources.google_drive.oauth import create_authorization_url
from app.sources.google_drive.oauth_state import oauth_states

from app.services import google_drive_service

def connect_google_drive(user_id: int):

    authorization_url, state, code_verifier = create_authorization_url()

    oauth_states[state] = {
        "user_id": user_id,
        "code_verifier": code_verifier
    }

    return {
        "authorization_url": authorization_url
    }



def google_drive_callback(code: str, state: str):

    # --------------------------------------------------
    # 1. Verify OAuth state
    # --------------------------------------------------

    oauth_data = oauth_states.pop(state, None)

    if oauth_data is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OAuth state"
        )

    user_id = oauth_data["user_id"]
    code_verifier = oauth_data["code_verifier"]

    # --------------------------------------------------
    # 2. Exchange authorization code for credentials
    # --------------------------------------------------

    try:
        credentials = exchange_code_for_credentials(code, state,code_verifier)

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

    existing_source = db_services.get_source_by_type(
        "google_drive"
    )

    # --------------------------------------------------
    # 5. Create or update source
    # --------------------------------------------------

    try:

        if existing_source:

            source = db_services.update_source(
                source_id=existing_source.id,
                status="connected",
                account_email=account_email
            )

        else:

            source = db_services.create_source(
                source_type="google_drive",
                name="Google Drive",
                status="connected",
                account_email=account_email
            )

        # --------------------------------------------------
        # 6. Save OAuth credentials
        # --------------------------------------------------

        existing_credentials = (
            db_services.get_source_credentials_by_source_id(
                source.id
            )
        )

        if existing_credentials:

            db_services.update_source_credentials(
                source_id=source.id,
                access_token=credentials.token,
                refresh_token=(
                    credentials.refresh_token
                    or existing_credentials.refresh_token
                ),
                token_expiry=credentials.expiry
            )

        else:

            db_services.create_source_credentials(
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
            f"http://localhost:5173/")
    )


def get_sources():
    sources = db_services.get_sources()
    return {
    "sources": [
        {
            "id": source.id,
            "type": source.type,
            "name": source.name,
            "status": source.status,
            "account_email": source.account_email,
        }
        for source in sources
    ]
    }


def disconnect_google_drive():

    source = db_services.get_source_by_type("google_drive")

    if not source:
        raise HTTPException(
            status_code=404,
            detail="Google Drive is not connected"
        )

    credentials = db_services.get_source_credentials_by_source_id(
        source.id
    )

    if credentials:
        try:
            revoke_google_credentials(
                credentials.refresh_token
                or credentials.access_token
            )

        except Exception as error:
            print(f"Google token revocation failed: {error}")

            raise HTTPException(
                status_code=500,
                detail="Failed to revoke Google Drive authorization"
            )

        db_services.delete_source_credentials(source.id)

    db_services.delete_source(source.id)

    return {
        "message": "Google Drive disconnected successfully"
    }


def get_google_drive_picker_token():
    source = db_services.get_source_by_type("google_drive")

    if not source:
        raise HTTPException(
            status_code=404,
            detail="Google Drive is not connected"
        )

    credentials = db_services.get_source_credentials_by_source_id(source.id)

    if not credentials:
        raise HTTPException(
            status_code=404,
            detail="Google Drive credentials not found"
        )

    access_token = google_drive_service.get_valid_access_token(
        credentials
    )

    return {
        "access_token": access_token
    }


def post_google_drive_root_folder(folder_id, user_id):
    source = db_services.get_source_by_type("google_drive")

    if not source:
        raise HTTPException(
            status_code=404,
            detail="Google Drive is not connected"
        )

    credentials = db_services.get_source_credentials_by_source_id(
        source.id
    )

    if not credentials:
        raise HTTPException(
            status_code=404,
            detail="Google Drive credentials not found"
        )

    folder = google_drive_service.get_folder(
        credentials,
        folder_id
    )

    if not folder:
        raise HTTPException(
            status_code=404,
            detail="Google Drive folder not found"
        )

    if folder["mimeType"] != "application/vnd.google-apps.folder":
        raise HTTPException(
            status_code=400,
            detail="Selected item is not a folder"
        )

    updated_source = db_services.update_source_root_folder(
        source.id,
        folder["id"],
        folder["name"]
    )

    return {
        "message": "Google Drive root folder selected successfully",
        "folder": {
            "id": updated_source.root_folder_id,
            "name": updated_source.root_folder_name
        }
    }  