from pydantic import BaseModel, Field

class RootFolderRequest(BaseModel):
    folder_id: str

class SyncRequest(BaseModel):
    external_file_ids: list[str]