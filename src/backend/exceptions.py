import logging

from fastapi.exceptions import HTTPException
from httpx import HTTPStatusError
from starlette import status

logger = logging.getLogger(__name__)


class BaseAPIException(HTTPException):
    status_code: status
    error: str

    def __init__(self, detail: str) -> None:
        self.detail = detail

    def __repr__(self) -> str:
        return f"Error: {self.error}, status: {self.status_code}, detail: {self.detail}"


class NotFoundError(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    error = "Not found"


class AlreadyExistError(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    error = "Already exist"


class UserNotAuthorised(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error = "User is not authorized"


class GoneError(BaseAPIException):
    status_code = status.HTTP_410_GONE
    error = "expired or inactive"


class UnAvailableError(BaseAPIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error = "service unaviable"


class BadRequestError(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "bad request"


class ServerError(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error = "Упс! Что-то пошло не так ;("


def raise_httpx_exception(err: HTTPStatusError) -> None:
    logger.error(f"error: {err}")
    message = f"status_code: {err.response.status_code}, phrase: {err.response.json()}"
    if err.response.status_code == 404:
        raise NotFoundError(message)
    elif err.response.status_code == 400:
        raise BadRequestError(message)
    else:
        raise err
