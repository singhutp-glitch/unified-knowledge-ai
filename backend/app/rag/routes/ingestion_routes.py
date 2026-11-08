from fastapi import APIRouter, Depends, File, UploadFile

from app.dependencies.auth import get_current_user
from app.rag.controllers import ingestion 
from app.rag.controllers import retrieval 
from app.schemas.rag import RetrievalRequest

router = APIRouter(tags=["RAG"])


@router.post("/chats/{chat_id}/documents")
def upload_document(
    chat_id: int,
    document: UploadFile = File(...),
    user_id: int = Depends(get_current_user)
):
    return ingestion.post_upload_document(
        document,
        chat_id,
        user_id
    )


@router.post("/chats/{chat_id}/chunks")
async def get_chunks(
    data:RetrievalRequest,
    chat_id: int,
    user_id: int = Depends(get_current_user)
):
    return await retrieval.get_chunks(
        data,
        chat_id,
        user_id
    )