from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.services import db_services
from app.rag.retrieval.dense.dense_retrieval import retrieve_dense
from app.rag.retrieval.fulltext.fulltext_retrieval import retrieve_fulltext
from app.rag.retrieval.hybrid.hybrid_retrieval import retrieve_hybrid
from app.schemas.rag import RetrievalRequest

async def get_chunks(
    data:RetrievalRequest,
    chat_id: int,
    user_id: int
):
    try:
        query = data.message

        # Verify that the chat belongs to the authenticated user
        user_chat = db_services.search_chat_id_with_user_id(
            user_id,
            chat_id
        )

        if not user_chat:
            raise HTTPException(
                status_code=404,
                detail="Chat not found"
            )

        if not query:
            raise HTTPException(
                status_code=400,
                detail="Query is required"
            )

        chunk_results = await retrieve_hybrid(
            query,
            chat_id
        )

        return {
            "message": "Retrieval successful",
            "chunkResults": chunk_results
        }

    except HTTPException:
        raise

    except Exception as error:
        import traceback
        print("Error:", error)
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Error while retrievel"
        )