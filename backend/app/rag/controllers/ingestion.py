import os
from uuid import uuid4
import traceback
from fastapi import HTTPException, UploadFile

from app.services import db_services
from app.rag.services.storage_service import upload_document
from app.rag.parsers.parser_factory import parse_document
from app.rag.chunker.chunk_document import chunk_document
from app.rag.embeddings.generate_embeddings import generate_embeddings
from app.rag.services.save_document_and_chunks import save_document_and_chunks


async def post_upload_document(
    document: UploadFile,
    chat_id: int,
    user_id: int
):
    if not document:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded"
        )

    try:
        # Check whether chat belongs to the authenticated user
        user_chat = db_services.search_chat_id_with_user_id(
            user_id,
            chat_id
        )

        if not user_chat:
            raise HTTPException(
                status_code=404,
                detail="Chat not found"
            )

        # Read uploaded file
        file_content = await document.read()
        document.file_content = file_content

        # Upload/store the document
        file_path = upload_document(
            file_content,
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
        parsed_document = await parse_document(document)

        # Chunk document
        chunks = await chunk_document(
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
        final_chunks = await generate_embeddings(
            chunks
        )

        # Save document and chunks
        saved_document = save_document_and_chunks(
            {
                "originalname": document.filename,
                "mimetype": document.content_type,
                "size": document.size,
                "userId": user_id,
                "chatId": chat_id,
                "storedFileName": stored_file_name
            },
            chunks
        )

        return {
            "message": "Upload successful",
            "documentContent": chunk_text
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Error:", error)
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Error in uploading file"
        )