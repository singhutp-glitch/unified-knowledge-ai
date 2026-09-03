from app.rag.embeddings.gemini_embedding import gemini_embedding


async def generate_embeddings(chunks):

    batch_size = 50
    all_embeddings = []

    for i in range(0, len(chunks), batch_size):

        batch = chunks[i:i + batch_size]

        texts = [
            {
                "parts": [
                    {
                        "text": (
                            f"Section: "
                            f"{chunk.get('sectionHeading') or 'Unknown'}"
                            f"\n\n"
                            f"{chunk['text']}"
                        )
                    }
                ]
            }
            for chunk in batch
        ]

        embeddings = await gemini_embedding(texts)

        if len(embeddings) != len(batch):
            raise ValueError("Embedding count mismatch")

        all_embeddings.extend(embeddings)

    if len(all_embeddings) != len(chunks):
        raise ValueError("Missing embeddings")

    for index, chunk in enumerate(chunks):
        chunk["embedding"] = all_embeddings[index]

    return chunks