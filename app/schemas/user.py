from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from app.models import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenData(BaseModel):
    id: int | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]
    name: str
    surname: str
    phone_number: str
    patronym: str | None = None
    role: UserRole = UserRole.PATIENT


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    phone_number: str
    role: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
