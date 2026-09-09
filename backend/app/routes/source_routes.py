from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.auth.dependencies import get_current_user
from app.controllers import source_controller


router = APIRouter(prefix="/sources", tags=["sources"])

@router.get("/google-drive/connect")
def connect_google_drive(user_id: int = Depends(get_current_user)):
    return source_controller.connect_google_drive(user_id)

@router.get("/google-drive/callback")
def google_drive_callback(
    code: str,
    state: str,
):
    return source_controller.google_drive_callback(code, state)