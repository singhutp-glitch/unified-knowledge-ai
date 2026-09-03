from fastapi import APIRouter, Depends, File, UploadFile

from app.dependencies.auth import get_current_user
from app.rag.controllers import ingestion as rag_controller


router = APIRouter(tags=["RAG"])


@router.post("/chats/{chat_id}/documents")
async def upload_document(
    chat_id: int,
    document: UploadFile = File(...),
    user_id: int = Depends(get_current_user)
):
    return await rag_controller.post_upload_document(
        document,
        chat_id,
        user_id
    )


@router.post("/chats/{chat_id}/chunks")
async def get_chunks(
    chat_id: int,
    user_id: int = Depends(get_current_user)
):
    return await rag_controller.get_chunks(
        chat_id,
        user_id
    )