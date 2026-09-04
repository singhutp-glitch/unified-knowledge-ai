from fastapi import HTTPException

from app.services import db_services


def get_chunks(chunk_id: int,user_id:int):

    try:
        chunk = db_services.load_chunk(
            chunk_id
        )

        return chunk

    except Exception as error:
        print("Error:", error)

        raise HTTPException(
            status_code=500,
            detail="Failed to load messages"
        )