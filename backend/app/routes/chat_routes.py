from fastapi import APIRouter, Depends

from app.controllers import chats_controller
from app.dependencies.auth import get_current_user
from app.schemas.chats import CreateChatRequest


router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/")
def load_chats(
    user_id: int = Depends(get_current_user)
):
    return chat_controller.load_chats_get(user_id)

@router.post("/")
def create_chat(
    data: CreateChatRequest,
    user_id: int = Depends(get_current_user)
):
    return chat_controller.create_chat_post(
        data,
        user_id
    )


@router.get("/{chat_id}/messages")
def load_messages(
    chat_id: int,
    user_id: int = Depends(get_current_user)
):
    return chat_controller.load_messages_get(
        chat_id,
        user_id
    )


@router.post("/{chat_id}/messages")
def send_message(
    chat_id: int,
    user_id: int = Depends(get_current_user)
):
    return chat_controller.send_message(
        chat_id,
        user_id
    )