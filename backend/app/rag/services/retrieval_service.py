from sqlalchemy import select

from app.models import Chunk, Document
from app.services.database import SessionLocal


def retrieve_chunks(
    query_embedding,
    chat_id: int,
    top_k: int = 10
):
    with SessionLocal() as db:

        stmt = (
            select(
                Chunk.id.label("id"),
                Chunk.document_id.label("documentId"),
                Chunk.text,
                Chunk.chunk_index.label("chunkIndex"),
                Document.original_file_name.label("originalFileName"),
                Chunk.pages,
                Chunk.type,
                Chunk.section_heading.label("sectionHeading"),
                Chunk.embedding.cosine_distance(
                    query_embedding
                ).label("score")
            )
            .join(
                Document,
                Document.id == Chunk.document_id
            )
            .where(
                Document.chat_id == chat_id
            )
            .order_by(
                "score"
            )
            .limit(top_k)
        )

        results = db.execute(stmt).mappings().all()

        return [dict(row) for row in results]