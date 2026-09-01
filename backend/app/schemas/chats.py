from pydantic import BaseModel, Field

class CreateChatRequest(BaseModel):
    message: str

class SendMessageRequest(BaseModel):
    message: str
    document_search: bool = Field(
        default=False,
        alias="documentSearch"
    )

    model_config = {
        "populate_by_name": True
    }