from app.database import SessionLocal
from app.models import User


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