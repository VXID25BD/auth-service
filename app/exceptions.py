from typing import Any, List

from fastapi import status


class ApiError(Exception):
    status_code: int
    errors: List[Any] | None
    detail: Any = None

    def __init__(self, status_code: status, detail: Any = None, errors: List[Any] | None = None, name: str = "Error"):
        self.status_code: int = status_code
        self.errors: List[Any] | None = errors
        self.detail: Any = detail
        self.name = name

    @staticmethod
    def unauthorized_error():
        return ApiError(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")

    @staticmethod
    def bad_request(detail, errors: List[Any] | None = None):
        return ApiError(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, errors=errors)
