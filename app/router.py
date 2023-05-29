from typing import Annotated

from fastapi import APIRouter, Depends, Header, Response, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, models
from app.database import get_db
from app.services import UserService
from app.services.user import settings
from app.utils import get_user

router: APIRouter = APIRouter()


@router.post("/registration", response_model=schemas.RegistrationCreate, status_code=status.HTTP_201_CREATED)
async def registration(
        registration_operation: schemas.RegistrationOperation,
        user_agent: Annotated[str, Header()],
        host: Annotated[str, Header()],
        response: Response,
        db: AsyncSession = Depends(get_db),
):
    access_token, refresh_session, email = await UserService.registration(
        db=db,
        registration_operation=registration_operation,
        user_agent=user_agent,
        ip=host
    )
    user: models.User = await get_user(db=db, email=email)
    response.set_cookie(
        key="refresh_token",
        value=refresh_session.refresh_token,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        samesite="strict"
    )
    return schemas.RegistrationCreate(
        user=user,
        access_token=access_token
    )


@router.post("/login", response_model=schemas.Login, status_code=status.HTTP_200_OK)
async def login(
        login_operation: schemas.LoginOperation,
        user_agent: Annotated[str, Header()],
        host: Annotated[str, Header()],
        response: Response,
        db: AsyncSession = Depends(get_db),
):
    access_token, refresh_session, email = await UserService.login(
        login_operation=login_operation,
        user_agent=user_agent,
        ip=host,
        db=db
    )
    user: models.User = await get_user(db=db, email=email)
    response.set_cookie(
        key="refresh_token",
        value=refresh_session.refresh_token,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        samesite="strict"
    )
    return schemas.Login(
        user=user,
        access_token=access_token
    )


@router.get("/logout", response_model=schemas.UserCreate)
async def logout():
    pass


@router.get("/refresh", response_model=schemas.UserCreate)
async def refresh():
    pass
