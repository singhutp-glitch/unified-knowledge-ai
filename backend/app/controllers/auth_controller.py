from fastapi import HTTPException

from app.schemas.auth import LoginRequest
from app.services import db_services
from app.services.auth_service import verify_password, create_access_token

from sqlalchemy.orm import Session
from app.services import db_services

from app.models import User
from app.schemas.auth import SignupRequest
from app.services.auth_service import hash_password

def signup(
    data: SignupRequest
):

    existing_user = db_services.get_user_by_email(
        data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = db_services.create_user(
        data.name,
        data.email,
        password_hash
    )

    return {
        "message": "User created successfully",
        "user_id": user.id
    }


def login(data: LoginRequest):

    user = db_services.get_user_by_email(
        data.email
    )
    print("login started")
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }