from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.documents import router as documents_router
from app.routes.chats import router as chats_router
from app.routes.auth import router as auth_router
from app.routes.rag import router as rag_router

app = FastAPI(title="Unified Knowledge AI")


app.include_router(health_router, prefix="/health")
app.include_router(documents_router, prefix="/documents")
app.include_router(chats_router, prefix="/chats")
app.include_router(auth_router, prefix="/auth")
app.include_router(rag_router, prefix="/rag")