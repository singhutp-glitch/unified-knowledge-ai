from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.controllers import document_controller


router = APIRouter()


@router.get("/chunks/{chunk_id}")
def get_chunks(
    chunk_id: int,
    user_id: int = Depends(get_current_user)
):
    return document_controller.get_chunks(
        chunk_id,
        user_id
    )