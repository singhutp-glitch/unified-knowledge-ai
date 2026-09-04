from pydantic import BaseModel


class RetrievalRequest(BaseModel):
    message: str