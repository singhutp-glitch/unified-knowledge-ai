from fastapi import APIRouter, Depends, HTTPException

from app.controller import auth_controller


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

router.post("/signup")(auth_controller.signup)
router.post("/login")(auth_controller.login)