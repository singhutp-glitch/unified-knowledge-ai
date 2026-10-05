from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.dependencies.auth import get_current_user
from app.controllers import source_controller

from app.schemas.source import (RootFolderRequest)


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
def get_picker_token(
    user_id: int = Depends(get_current_user)
):
    return source_controller.get_google_drive_picker_token()

@router.post("/google-drive/root-folder")
def post_root_folder(
    data: RootFolderRequest,
    user_id: int = Depends(get_current_user)
):
    return source_controller.post_google_drive_root_folder(
        data.folder_id,
        user_id
    )

@router.delete("/google-drive/root-folder")
def post_root_folder(
    user_id: int = Depends(get_current_user)
):
    return source_controller.delete_google_drive_root_folder()