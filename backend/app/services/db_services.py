from app.models import Citation

from app.services.database import SessionLocal
from app.models import User
from app.models import Chat
from app.models import Message

def get_user_by_email(email: str):
    with SessionLocal() as db:
        return db.query(User).filter(
            User.email == email
        ).first()


def get_user_by_id(user_id: int):
    with SessionLocal() as db:
        return db.query(User).filter(
            User.id == user_id
        ).first()


def create_user(name: str, email: str, password_hash: str):
    with SessionLocal() as db:

        user = User(
            name=name,
            email=email,
            password_hash=password_hash
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

def load_chats(user_id:int):
    with SessionLocal() as db:
        return db.query(Chat).filter(
            Chat.user_id == user_id
        )



def create_new_chat(user_id: int, title: str):

    title = title.strip()[:60]

    with SessionLocal() as db:

        chat = Chat(
            title=title,
            user_id=user_id
        )

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return chat

def search_chat_id_with_user_id(user_id:int, chat_id:int):
    with SessionLocal() as db:
        return db.query(Chat).filter(
            Chat.id == chat_id,
            Chat.user_id == user_id
        ).first()


def load_messages(chat_id: int):

    with SessionLocal() as db:

        messages = (
            db.query(Message)
            .options(
                selectinload(Message.citations)
            )
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
            .all()
        )

        return [
            {
                "role": message.role,
                "content": message.content,
                "citations": [
                    {
                        "citationNumber": citation.citation_number,
                        "chunkId": citation.chunk_id
                    }
                    for citation in message.citations
                ]
            }
            for message in messages
        ]


def save_message(chat_id: int,role:str,content:str):

    with SessionLocal() as db:

        message = Message(
            id=chat_id,
            role=role,
            content=content
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return chat



def save_citations(chunk_results, message_id: int):
    try:
        if chunk_results:

            citations = [
                Citation(
                    message_id=message_id,
                    citation_number=int(chunk["citationNumber"]),
                    chunk_id=chunk["id"]
                )
                for chunk in chunk_results.values()
            ]

            with SessionLocal() as db:
                db.add_all(citations)
                db.commit()

    except Exception as error:
        print(error)