from datetime import timedelta, datetime
from typing import Dict, Any, Tuple
from uuid import uuid4

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, models
from app.config import Settings
from app.utils import get_refresh_session, update_refresh_session, create_refresh_session

settings: Settings = Settings(".env")


class TokenService:
    @staticmethod
    async def generate_tokens(
            user: models.User,
            fingerprint: str,
            user_agent: str,
            ip: str
    ) -> Tuple[str, schemas.RefreshSessionCreate]:
        """
        Generate access and refresh session.
        :param user: model user.
        :param fingerprint: user fingerprint.
        :param user_agent: request user_agent.
        :param ip: request ip.
        :return: tuple with access token and supplemented refresh session for create.
        """
        to_encode: Dict[str, Any] = {
            "user_id": user.id,
            "user_email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "surname": user.surname,
            "user_role": user.role,
            "user_bio": user.bio,
            "is_activated": user.is_activated,
            "fingerprint": fingerprint,
            "user_agent": user_agent,
            "ip": ip
        }
        to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)})
        access_token: str = jwt.encode(to_encode, settings.JWT_ACCESS_SECRET, algorithm=settings.ALGORITHM)

        expired_at: datetime = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        refresh_session: schemas.RefreshSessionCreate = schemas.RefreshSessionCreate(
            refresh_token=uuid4(),
            user_id=user.id,
            email=user.email,
            ip=ip,
            user_agent=user_agent,
            fingerprint=fingerprint,
            created_at=datetime.utcnow(),
            expired_at=expired_at
        )

        return access_token, refresh_session

    @staticmethod
    async def save_token(
            db: AsyncSession,
            refresh_session_create: schemas.RefreshSessionCreate
    ) -> models.RefreshSession:
        """
        Save the token in the DB, if a token with the same signature already exists, replace it.
        :param db: Async session DB.
        :param refresh_session_create: schema refresh session for create.
        :return: model refresh session.
        """
        refresh_session: models.RefreshSession = await get_refresh_session(
            db=db,
            user_id=refresh_session_create.user_id,
            ip=refresh_session_create.ip,
            fingerprint=refresh_session_create.fingerprint,
            user_agent=refresh_session_create.user_agent,
        )
        if refresh_session:
            await update_refresh_session(
                db=db,
                refresh_session_id=refresh_session.id,
                refresh_session_create=refresh_session_create
            )
            refresh_session: models.RefreshSession = await get_refresh_session(
                db=db,
                user_id=refresh_session_create.user_id,
                ip=refresh_session_create.ip,
                fingerprint=refresh_session_create.fingerprint,
                user_agent=refresh_session_create.user_agent,
            )
            return refresh_session

        refresh_session: models.RefreshSession = await create_refresh_session(
            db=db,
            refresh_session_create=refresh_session_create
        )
        return refresh_session
