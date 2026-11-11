from sqlalchemy import select, func

from app.models import Chunk, Document
from app.services.database import SessionLocal
from typing import Literal

def retrieve_dense_chunks(
    query_embedding,
    knowledge_scope: Literal["chat", "user", "company"],
    chat_id: int | None = None,
    user_id: int | None = None,
    top_k: int = 10
):
    with SessionLocal() as db:

        distance = Chunk.embedding.cosine_distance(
            query_embedding
        ).label("score")

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
                distance
            )
            .join(
                Document,
                Document.id == Chunk.document_id
            )
            .where(
                Chunk.embedding.is_not(None)
            )
        )

        # Search documents belonging to the current chat
        if knowledge_scope == "chat":

            if chat_id is None:
                raise ValueError("chat_id is required for chat scope")

            stmt = stmt.where(
                Document.chat_id == chat_id,
                ~Document.company_details.has()
            )

        # Search all documents belonging to the current user
        elif knowledge_scope == "user":

            if user_id is None:
                raise ValueError("user_id is required for user scope")

            stmt = stmt.where(
                Document.user_id == user_id,
                Document.user_id.is_not(None),
                ~Document.company_details.has()
            )

        # Search company documents
        elif knowledge_scope == "company":

            stmt = stmt.where(
                Document.company_details.has()
            )

        else:
            raise ValueError(f"Invalid knowledge scope: {knowledge_scope}")

        stmt = (
            stmt
            .order_by(distance)
            .limit(top_k)
        )

        results = db.execute(stmt).mappings().all()

        return [dict(row) for row in results]

def retrieve_fulltext_chunks(
    query: str,
    knowledge_scope: Literal["chat", "user", "company"],
    chat_id: int | None = None,
    user_id: int | None = None,
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
                Document.original_file_name.label("originalFileName"),
                Chunk.pages,
                Chunk.type,
                Chunk.section_heading.label("sectionHeading"),
                score.label("score")
            )
            .join(
                Document,
                Document.id == Chunk.document_id
            )
            .where(
                Chunk.search_vector.bool_op("@@")(ts_query)
            )
        )

        # Chat knowledge scope
        if knowledge_scope == "chat":

            if chat_id is None:
                raise ValueError("chat_id is required for chat scope")

            stmt = stmt.where(
                Document.chat_id == chat_id,
                ~Document.company_details.has()
            )

        # User knowledge scope
        elif knowledge_scope == "user":

            if user_id is None:
                raise ValueError("user_id is required for user scope")

            stmt = stmt.where(
                Document.user_id == user_id,
                Document.user_id.is_not(None),
                ~Document.company_details.has()
            )

        # Company knowledge scope
        elif knowledge_scope == "company":

            stmt = stmt.where(
                Document.company_details.has()
            )

        else:
            raise ValueError(
                f"Invalid knowledge scope: {knowledge_scope}"
            )

        stmt = (
            stmt
            .order_by(score.desc())
            .limit(top_k)
        )

        results = db.execute(stmt).mappings().all()

        return [dict(row) for row in results]