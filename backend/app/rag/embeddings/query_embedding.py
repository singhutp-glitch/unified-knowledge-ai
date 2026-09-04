from app.rag.embeddings.gemini_embeddings import gemini_query_embedding


async def generate_query_embeddings(query):
    embedding = await gemini_query_embedding(query)

    return embedding