from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserRole(str, Enum):
    UNAUTHENTICATED = "unauthenticated"
    USER = "user"
    ADMIN = "admin"


class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    role: Optional[UserRole] = None


class UserInDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    role: UserRole
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None


class LoginRequest(BaseModel):
    username: str
    password: str