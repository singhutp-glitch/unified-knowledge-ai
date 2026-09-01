from fastapi import APIRouter

from app.controllers.health_controller import health

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_route():
    return health()