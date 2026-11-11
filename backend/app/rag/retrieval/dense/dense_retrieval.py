from app.rag.embeddings.query_embedding import generate_query_embeddings
from app.rag.services.retrieval_service import retrieve_dense_chunks


async def retrieve_dense(
    query,
    knowledge_scope,
    chat_id,
    user_id,
    top_k=10
):
    query_embedding = await generate_query_embeddings(
        query
    )

    chunk_results = retrieve_dense_chunks(
        query_embedding,
        knowledge_scope,
        chat_id,
        user_id,
        top_k
    )

    return chunk_results