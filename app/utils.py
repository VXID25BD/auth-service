from typing import Dict, Any
from passlib.context import CryptContext
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.schemas import RefreshSessionCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


async def create_user(db: AsyncSession, user: Dict[str, Any]) -> models.User:
    db_model = models.User(**user)
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return db_model


async def get_user(db: AsyncSession, email: str) -> models.User:
    stml = select(models.User).where(models.User.email == email)
    result = await db.execute(stml)
    return result.scalars().first()


async def get_refresh_session(db: AsyncSession, user_id: int, ip: str, fingerprint: str, user_agent: str):
    stml = (
        select(models.RefreshSession).
        where(
            models.RefreshSession.user_id == user_id,
            models.RefreshSession.ip == ip,
            models.RefreshSession.fingerprint == fingerprint,
            models.RefreshSession.user_agent == user_agent
        )
    )
    result = await db.execute(stml)
    return result.scalars().first()


async def create_refresh_session(db: AsyncSession, refresh_session_create: RefreshSessionCreate):
    db_model = models.RefreshSession(**refresh_session_create.dict(exclude_unset=True))
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return db_model


async def update_refresh_session(
        db: AsyncSession,
        refresh_session_id: int,
        refresh_session_create: RefreshSessionCreate
):
    stml = (
        update(models.RefreshSession).
        where(models.RefreshSession.id == refresh_session_id).
        values(refresh_session_create.dict(exclude_unset=True))
    )
    result = await db.execute(stml)
    await db.commit()
