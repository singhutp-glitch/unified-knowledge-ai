from pydantic import BaseModel , EmailStr, Field

class SignupRequest(BaseModel):
    name:str
    email:EmailStr
    password:str
    is_admin: bool = Field(
        default=False,
        alias="isAdmin"
    )
    admin_code: str | None = Field(
        default=None,
        alias="adminCode"
    )
class TokenResponse(BaseModel):
    access_token:str
    token_type:str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str