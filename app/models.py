from datetime import datetime

from uuid import UUID

from pydantic import HttpUrl, EmailStr
from sqlalchemy import ForeignKey, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.constants import UserRole, UserStatus
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[EmailStr] = mapped_column(String, nullable=False, unique=True)
    password_hashed: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str | None] = mapped_column(String, nullable=True)
    vk: Mapped[HttpUrl | None] = mapped_column(String, nullable=True, unique=True)
    steam: Mapped[HttpUrl | None] = mapped_column(String, nullable=True, unique=True)
    registered_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    role: Mapped[UserRole] = mapped_column(String, default=UserRole.USER)
    is_activated: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default=UserStatus.ACTIVE)


class RefreshSession(Base):
    __tablename__ = "refresh_session"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    refresh_token: Mapped[UUID] = mapped_column(PG_UUID, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    ip: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    user_agent: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    fingerprint: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    expired_at: Mapped[datetime] = mapped_column(TIMESTAMP, unique=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, unique=False)
