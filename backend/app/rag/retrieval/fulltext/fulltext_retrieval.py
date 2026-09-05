from sqlalchemy import func, select

from app.models import Chunk, Document

from app.rag.services.retrieval_service import retrieve_fulltext_chunks

async def retrieve_fulltext(
    query,
    chat_id,
    top_k=10
):
    chunk_results = retrieve_fulltext_chunks(
        query,
        chat_id,
        top_k
    )

    return chunk_results