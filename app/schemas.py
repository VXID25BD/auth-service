from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl

from app.constants import UserRole, UserStatus


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    surname: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    bio: str | None = None
    vk: HttpUrl | None = None
    steam: HttpUrl | None = None
    registered_at: datetime
    is_activated: bool = False
    role: str | UserRole = UserRole.USER
    status: str | UserStatus = UserStatus.ACTIVE

    class Config:
        orm_mode = True


class RefreshSessionBase(BaseModel):
    ip: str
    user_agent: str
    fingerprint: str


class RefreshSessionCreate(RefreshSessionBase):
    user_id: int
    refresh_token: UUID
    expired_at: datetime
    created_at: datetime


class RefreshSession(RefreshSessionBase):
    id: int
    user_id: int
    refresh_token: UUID
    expired_at: datetime
    created_at: datetime


class OperationBase(BaseModel):
    fingerprint: str


class RegistrationOperation(OperationBase):
    user: UserCreate


class RegistrationCreate(BaseModel):
    user: User
    access_token: str


class LoginOperation(OperationBase):
    user: UserLogin


class Login(BaseModel):
    user: User
    access_token: str
