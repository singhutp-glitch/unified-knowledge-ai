from app.schemas.auth import SignupRequest, LoginRequest

from fastapi import APIRouter, Depends, HTTPException

from app.controllers import auth_controller


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register")
def register(data: SignupRequest):
    return auth_controller.signup(data)


@router.post("/login")
def login(data: LoginRequest):
    return auth_controller.login(data)