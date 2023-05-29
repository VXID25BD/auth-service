from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import sessionmanager
from config import config_db


def init_app(init_db=True) -> FastAPI:
    lifespan = None

    if init_db:
        sessionmanager.init(config_db.DSN)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    app: FastAPI = FastAPI(title="FastAPI server", lifespan=lifespan)

    from app.router import router as auth_router

    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    return app
