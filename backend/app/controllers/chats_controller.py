import json
from fastapi.responses import StreamingResponse

from app.services import db_services
from app.pipeline.pipeline import build_pipeline_context
from app.services.gemini_service import generate_response_stream
from app.schemas.chats import (SendMessageRequest,CreateChatRequest)
from fastapi import HTTPException

def load_chats_get(user_id: int):

    try:
        user_chats = db_services.load_chats(user_id)

        return user_chats

    except Exception as error:
        print(error)

        raise HTTPException(
            status_code=500,
            detail="Failed to load chats"
        )



def create_chat_post(
    data: CreateChatRequest,
    user_id: int
):
    try:
        prompt = data.message

        if not prompt or not prompt.strip():
            raise HTTPException(
                status_code=400,
                detail="Prompt is required"
            )

        chat = db_services.create_new_chat(
            user_id,
            prompt
        )

        return {
            "chatId": chat.id
        }

    except HTTPException:
        raise

    except Exception as error:
        print(error)

        raise HTTPException(
            status_code=500,
            detail="Failed to create new chat"
        )

def load_messages_get(
    chat_id: int,
    user_id: int
):
    try:
        user_chat = db_services.search_chat_id_with_user_id(
            user_id,
            chat_id
        )

        if not user_chat:
            raise HTTPException(
                status_code=404,
                detail="Chat not found"
            )

        messages = db_services.load_messages(chat_id)

        return messages

    except HTTPException:
        raise

    except Exception as error:
        print(error)

        raise HTTPException(
            status_code=500,
            detail="Failed to load messages"
        )



async def send_message(
    data: SendMessageRequest,
    chat_id: int,
    user_id: int
):
    full_response = ""

    try:
        prompt = data.message
        document_search = data.documentSearch

        if not prompt or not prompt.strip():
            raise HTTPException(
                status_code=400,
                detail="Prompt is required"
            )

        # Verify that this chat belongs to the authenticated user
        user_chat = db_services.search_chat_id_with_user_id(
            user_id,
            chat_id
        )

        if not user_chat:
            raise HTTPException(
                status_code=404,
                detail="Chat not found"
            )

        # Save user's message
        await db_services.save_message(
            chat_id,
            "user",
            prompt
        )

        # Load previous messages
        messages = await db_services.load_messages(
            chat_id
        )

        # Build RAG pipeline context
        context = {
            "userMessages": messages,
            "userPrompt": prompt,
            "chatId": chat_id,
            "options": {
                "documentSearch": document_search
            },
            "documentSources": None,
            "metaData": {},
            "features": [],
            "contents": []
        }

        await build_pipeline_context(context)

        async def generate():

            nonlocal full_response

            # Send status message
            yield json.dumps({
                "type": "status",
                "status": "Generating..."
            }) + "\n"

            # Generate LLM response stream
            stream = await generate_response_stream(
                context["contents"]
            )

            for chunk in stream:

                text = getattr(chunk, "text", "") or ""

                full_response += text

                yield json.dumps({
                    "type": "token",
                    "text": text
                }) + "\n"

            # Save assistant response
            saved_message = await db_services.save_message(
                chat_id,
                "assistant",
                full_response
            )

            # Save citations
            await db_services.save_citations(
                context["documentSources"],
                saved_message.id
            )

        return StreamingResponse(
            generate(),
            media_type="application/x-ndjson"
        )

    except HTTPException:
        raise

    except Exception as error:

        print(error)

        async def error_stream():

            if full_response:
                await db_services.save_message(
                    chat_id,
                    "assistant",
                    full_response +
                    "\n\n[Response interrupted]"
                )
            else:
                await db_services.save_message(
                    chat_id,
                    "assistant",
                    "Failed to generate response"
                )

            yield json.dumps({
                "type": "error",
                "error": "Failed to generate response"
            }) + "\n"

        return StreamingResponse(
            error_stream(),
            media_type="application/x-ndjson"
        )