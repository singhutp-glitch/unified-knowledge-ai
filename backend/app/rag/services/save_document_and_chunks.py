from app.services.database import SessionLocal
from app.rag.services.chunk_service import save_chunks
from app.models import Document,CompanyDocument


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


def save_company_document_and_chunks(data, chunks):

    with SessionLocal() as db:
        try:
            document = Document(
                original_file_name=data["originalname"],
                mime_type=data["mimetype"],
                file_size=data["size"],
                user_id=None,
                chat_id=None,
                stored_file_name=data["storedFileName"],
                document_type="company"
            )

            db.add(document)
            db.flush()

            company_document = CompanyDocument(
                document_id=document.id,
                source_id=data["source_id"],
                external_file_id=data["external_file_id"],
                external_modified_at=data["external_modified_at"],
            )

            db.add(company_document)

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