from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID


class RegisterInSchema(BaseModel):
    email: EmailStr = Field(..., title=" User Email")
    password: str = Field(..., min_length=8, max_length=128,
                          title="account password")
    username: str | None = "None"


class RegesterOutSchema(BaseModel):
    email: EmailStr
    public_id: UUID
    username: str


class LoginInSchema(BaseModel):
    email: EmailStr = Field(..., title=" User Email")
    password: str = Field(..., min_length=8, max_length=128,
                          title="account password")


class LoginOutSchema(BaseModel):
    user_public_id: str
    email: EmailStr
    token_type: str = "bearer"
    massege: str = "login successful"
    R_token: str

    model_config = ConfigDict(from_attributes=True)


class UserOutSchema(BaseModel):
    public_id: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class DeleteAccountSchema(BaseModel):
    password: str = Field(..., min_length=8, max_length=128,
                          title="account password")
