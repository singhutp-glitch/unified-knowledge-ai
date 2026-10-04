from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.dependencies.auth import get_current_user
from app.controllers import source_controller


router = APIRouter( tags=["sources"])

@router.get("/google-drive/connect")
def connect_google_drive(user_id: int = Depends(get_current_user)):
    return source_controller.connect_google_drive(user_id)

@router.get("/google-drive/callback")
def google_drive_callback(
    code: str,
    state: str,
):
    return source_controller.google_drive_callback(code, state)

@router.get("/")
def get_sources(
    user_id: int = Depends(get_current_user)
):
    return source_controller.get_sources()


@router.delete("/google-drive")
def disconnect_google_drive(
    user_id: int = Depends(get_current_user)
):
    return source_controller.disconnect_google_drive()

@router.get("/google-drive/picker-token")
def get_sources(
    user_id: int = Depends(get_current_user)
):
    return source_controller.get_google_drive_picker_token()
