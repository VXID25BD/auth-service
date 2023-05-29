from typing import Tuple, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, models
from app.config import Settings
from app.exceptions import ApiError
from app.schemas import LoginOperation
from app.services.token import TokenService
from app.utils import get_password_hash, create_user, get_user, verify_password

settings: Settings = Settings(".env")


class UserService:
    @staticmethod
    async def registration(
            db: AsyncSession,
            user_agent: str,
            ip: str,
            registration_operation: schemas.RegistrationOperation
    ) -> Tuple[str, models.RefreshSession, str]:
        """
        Service for registration user.
        Create user in DB, access token, refresh session.
        :param ip: request ip.
        :param user_agent: request user-agent.
        :param db: Async session DB.
        :param registration_operation: schema that contains data for registration.
        :return: access token, refresh token and model user.
        """
        candidate: models.User = await get_user(db=db, email=registration_operation.user.email)

        if candidate:
            raise ApiError.bad_request(detail="User with this email address already exists.")

        password_hashed: str = await get_password_hash(registration_operation.user.password)
        user_dict: Dict[str, Any] = registration_operation.user.__dict__
        user_dict.pop("password")
        user_dict["password_hashed"] = password_hashed
        user: models.User = await create_user(db=db, user=user_dict)
        email: str = user.email

        access_token, refresh_session_create = await TokenService.generate_tokens(
            user=user,
            fingerprint=registration_operation.fingerprint,
            user_agent=user_agent,
            ip=ip
        )
        refresh_session: models.RefreshSession = await TokenService.save_token(
            db=db,
            refresh_session_create=refresh_session_create
        )
        return access_token, refresh_session, email

    @staticmethod
    async def login(
            db: AsyncSession,
            user_agent: str,
            ip: str,
            login_operation: LoginOperation
    ) -> Tuple[str, models.RefreshSession, str]:
        user: models.User = await get_user(db=db, email=login_operation.user.email)
        if not user:
            raise ApiError.bad_request(detail="No user found with this email address.")
        is_password_valid: bool = await verify_password(
            plain_password=login_operation.user.password,
            hashed_password=user.password_hashed
        )
        if not is_password_valid:
            raise ApiError.bad_request(detail="Invalid password.")
        email: str = user.email
        access_token, refresh_session_create = await TokenService.generate_tokens(
            user=user,
            fingerprint=login_operation.fingerprint,
            user_agent=user_agent,
            ip=ip
        )
        refresh_session: models.RefreshSession = await TokenService.save_token(
            db=db,
            refresh_session_create=refresh_session_create
        )

        return access_token, refresh_session, email
