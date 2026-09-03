from app.services.database import SessionLocal
from app.rag.services.chunk_service import save_chunks
from app.models import Document


def save_document_and_chunks(data, chunks):

    with SessionLocal() as db:
        try:
            document = Document(
                original_file_name=data["originalname"],
                mime_type=data["mimetype"],
                file_size=data["size"],
                user_id=data["userId"],
                chat_id=data["chatId"],
                stored_file_name=data["storedFileName"]
            )

            db.add(document)
            db.flush()

            save_chunks(
                db,
                chunks,
                document
            )

            db.commit()

            db.refresh(document)

            return document

        except Exception:
            db.rollback()
            raise