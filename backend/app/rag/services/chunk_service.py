from app.models import Chunk


def save_chunks(db, chunks, document):

    chunk_objects = [
        Chunk(
            document_id=document.id,
            chunk_index=chunk["index"],
            text=chunk["text"],
            pages=chunk["pages"],
            section_heading=chunk["sectionHeading"],
            type=chunk["type"],
            embedding=chunk["embedding"]
        )
        for chunk in chunks
    ]

    db.add_all(chunk_objects)
    db.flush()

    return chunk_objects

def delete_chunks(db, document_id: int):
    return (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .delete(synchronize_session=False)
    )