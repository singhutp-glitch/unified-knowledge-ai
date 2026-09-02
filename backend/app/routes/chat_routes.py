from fastapi import APIRouter, Depends

from app.controllers import chats_controller
from app.dependencies.auth import get_current_user
from app.schemas.chats import (CreateChatRequest ,SendMessageRequest)


router = APIRouter(
    tags=["Chats"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/")
def load_chats(
    user_id: int = Depends(get_current_user)
):
    return chats_controller.load_chats_get(user_id)

@router.post("/")
def create_chat(
    data: CreateChatRequest,
    user_id: int = Depends(get_current_user)
):
    return chats_controller.create_chat_post(
        data,
        user_id
    )


@router.get("/{chat_id}/messages")
def load_messages(
    chat_id: int,
    user_id: int = Depends(get_current_user)
):
    return chats_controller.load_messages_get(
        chat_id,
        user_id
    )


@router.post("/{chat_id}/messages")
async def send_message(
    data: SendMessageRequest,
    chat_id: int,
    user_id: int = Depends(get_current_user)
):
    return await chats_controller.send_message(
        data,
        chat_id,
        user_id
    )