from fastapi import FastAPI, Request, status, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from starlette.responses import JSONResponse
from app import init_app
from app.exceptions import ApiError

app: FastAPI = init_app()


@app.middleware("http")
async def error_middleware(request: Request, call_next) -> Response:
    try:
        response: Response = await call_next(request)
        return response
    except Exception as error:
        print(error)
        if isinstance(error, ApiError):
            return JSONResponse(
                content=jsonable_encoder({"message": error.detail, "errors": error.errors}),
                status_code=error.status_code
            )

        return JSONResponse(
            content=jsonable_encoder({"message": "Unexpected error"}),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"message": exc.errors(), "body": exc.body}),
    )
