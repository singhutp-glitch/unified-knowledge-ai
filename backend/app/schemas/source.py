from pydantic import BaseModel, Field

class RootFolderRequest(BaseModel):
    folder_id: str