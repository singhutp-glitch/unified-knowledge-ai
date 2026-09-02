from app.schemas.auth import SignupRequest, LoginRequest

from fastapi import APIRouter, Depends, HTTPException

from app.controllers import auth_controller
from app.dependencies.auth import get_current_user


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register")
def register(data: SignupRequest):
    return auth_controller.signup(data)


@router.post("/login")
def login(data: LoginRequest):
    return auth_controller.login(data)

@router.get("/me")
def send_user_info(
    user_id: int = Depends(get_current_user)
):
    return auth_controller.send_user_info(user_id)