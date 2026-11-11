import traceback
from fastapi import HTTPException

from app.schemas.auth import LoginRequest
from app.services import db_services
from app.services.auth_service import (verify_password, create_access_token,
verify_secret_admin_code)

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
    print("is admin in contoller ",data.is_admin)
    if(data.is_admin):
        result = verify_secret_admin_code(data.admin_code)
        if(not result):
            raise HTTPException(
            status_code=401,
            detail="Invalid admin code"
        )

    password_hash = hash_password(data.password)

    user = db_services.create_user(
        data.name,
        data.email,
        password_hash,
        data.is_admin
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
        user.id
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
         "user":{
                "name":user.name,
                "email":user.email,
                "role":user.role
            }
    }



def send_user_info(user_id: int):
    try:
        user = db_services.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }

    except HTTPException:
        raise

    except Exception as error:
        print(error)
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Server error"
        )