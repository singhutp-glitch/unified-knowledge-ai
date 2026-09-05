from sqlalchemy import select, func

from app.models import Chunk, Document
from app.services.database import SessionLocal


def retrieve_dense_chunks(
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


def retrieve_fulltext_chunks(
    query: str,
    chat_id: int,
    top_k: int = 10
):
    with SessionLocal() as db:

        ts_query = func.websearch_to_tsquery(
            "english",
            query
        )

        score = func.ts_rank(
            Chunk.search_vector,
            ts_query
        )

        stmt = (
            select(
                Chunk.id.label("id"),
                Chunk.document_id.label("documentId"),
                Chunk.text,
                Chunk.chunk_index.label("chunkIndex"),
                Document.original_file_name.label(
                    "originalFileName"
                ),
                Chunk.pages,
                Chunk.type,
                Chunk.section_heading.label(
                    "sectionHeading"
                ),
                score.label("score")
            )
            .join(
                Document,
                Document.id == Chunk.document_id
            )
            .where(
                Document.chat_id == chat_id
            )
            .where(
                Chunk.search_vector.bool_op("@@")(
                    ts_query
                )
            )
            .order_by(
                score.desc()
            )
            .limit(top_k)
        )

        results = db.execute(stmt).mappings().all()

        return [dict(row) for row in results]