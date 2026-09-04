from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.health_routes import router as health_router
from app.routes.document_routes import router as documents_router
from app.routes.chat_routes import router as chats_router
from app.routes.auth_routes import router as auth_router
from app.rag.routes.ingestion_routes import router as rag_router

app = FastAPI(title="Unified Knowledge AI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health")
app.include_router(documents_router, prefix="/documents")
app.include_router(chats_router, prefix="/chats")
app.include_router(auth_router, prefix="/auth")
app.include_router(rag_router, prefix="/rag")
