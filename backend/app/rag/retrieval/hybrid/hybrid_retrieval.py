from app.rag.retrieval.dense.dense_retrieval import retrieve_dense
from app.rag.retrieval.fulltext.fulltext_retrieval import retrieve_fulltext
from app.rag.retrieval.hybrid.rrf import reciprocal_rank_fusion


async def retrieve_hybrid(
    query,
    knowledge_scope,
    chat_id,
    user_id,
    top_k=10
):
    dense_chunk_results = await retrieve_dense(
        query,
        knowledge_scope,
        chat_id,
        user_id,
        20
    )

    fulltext_chunk_results = await retrieve_fulltext(
        query,
        knowledge_scope,
        chat_id,
        user_id,
        20
    )

    hybrid_chunk_results = reciprocal_rank_fusion([
        dense_chunk_results,
        fulltext_chunk_results
    ])

    chunk_map = {
        chunk["id"]: chunk
        for chunk in (
            dense_chunk_results + fulltext_chunk_results
        )
    }

    enriched_results = []

    for result in hybrid_chunk_results:

        chunk = chunk_map.get(
            result["id"]
        )

        if chunk is None:
            continue

        enriched_results.append({
            "id": result["id"],
            "score": result["score"],
            "rank": result["rank"],
            "text": chunk["text"],
            "sectionHeading": chunk["sectionHeading"],
            "originalFileName": chunk["originalFileName"],
            "type": chunk["type"],
            "pages":chunk["pages"]        
            })

    return enriched_results