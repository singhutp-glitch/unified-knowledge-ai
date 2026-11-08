from app.services.google_drive_service import download_drive_file
import io
from fastapi import UploadFile
from starlette.datastructures import Headers
import os
import logging
from uuid import uuid4
from datetime import datetime

from app.services import db_services
from app.rag.services.storage_service import upload_document
from app.rag.parsers.parser_factory import parse_document
from app.rag.chunker.chunk_document import chunk_document
from app.rag.embeddings.generate_embeddings import generate_embeddings
from app.rag.services.save_document_and_chunks import save_company_document_and_chunks



logger = logging.getLogger(__name__)


def add_company_document(change,credentials):
    try:
        downloaded_file = google_drive_service.download_drive_file(
        credentials,
        change["external_file_id"]
        )
       

        document = UploadFile(
        filename=downloaded_file["file_name"],
        file=io.BytesIO(downloaded_file["content"]),
        headers=Headers({
            "content-type": downloaded_file["downloaded_mime_type"]
        }))

        modified_at = download_drive_file["modified_time"]
        modified_at = datetime.fromisoformat(
                    modified_at.replace("Z", "+00:00")
                )

        file_content = downloaded_file["content"]
        document.file_content = file_content

        # Upload/store the document
        file_path = upload_document(
            document.file_content,
            document.filename
        )

        # Get extension
        extension = os.path.splitext(
            document.filename
        )[1]

        # Generate stored filename
        stored_file_name = f"{uuid4()}{extension}"

        # Put file path into the upload object if your parser expects it
        document.file_path = file_path

        # Parse document
        parsed_document = parse_document(document)

        # Chunk document
        chunks = chunk_document(
            parsed_document
        )

        # Build preview text
        chunk_text = "\n\n---\n\n".join(
            f"""
## Chunk {index}

**Type:** {chunk.get("type")}

**Pages:** {chunk.get("startPage")}{
    "" if chunk.get("endPage") == chunk.get("startPage")
    else f" - {chunk.get('endPage')}"
}

**Heading:** {chunk.get("sectionHeading")}

**Content:** 

{chunk.get("text")}
"""
            for index, chunk in enumerate(chunks[:30])
        )

        print("chunks - ",chunk_text[0:2000])

        # Generate embeddings
        final_chunks = generate_embeddings(
            chunks
        )

        # Save document and chunks
        saved_document = save_company_document_and_chunks(
            {
                "originalname": document.filename,
                "mimetype": document.content_type,
                "size": document.size,
                "storedFileName": stored_file_name,
                "source_id":credentials.source_id,
                "external_file_id":change.external_file_id,
                "external_modified_at":modified_at
            },
            chunks
        )

        return 

    except Exception:
        logger.exception(
            "Failed to add company document: %s",
            change["external_file_id"]
        )
        raise



def update_company_document(change):
    # Download the updated Google Drive file
    # Extract its content
    # Generate new chunks and embeddings
    # Update the existing company document
    # Replace its previous chunks and vectors
    pass


def remove_company_document(change):
    # Find the existing company document
    # Remove or deactivate it
    # Remove its associated chunks and vectors
    pass