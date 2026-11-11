from pydantic import BaseModel, Field

class CreateChatRequest(BaseModel):
    message: str

from typing import Literal
from pydantic import BaseModel, Field

class SendMessageRequest(BaseModel):
    message: str

    document_search: bool = Field(
        default=False,
        alias="documentSearch"
    )

    knowledge_scope: Literal["chat", "user", "company","nofile"] = Field(
        default="chat",
        alias="knowledgeScope"
    )

    model_config = {
        "populate_by_name": True
    }