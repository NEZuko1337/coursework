from fastapi.exceptions import HTTPException

from starlette import status


class BaseAPIException(HTTPException):
    status_code: status
    error: str

    def __init__(self, detail: str) -> None:
        self.detail = detail

    def __repr__(self) -> str:
        return f"Error: {self.error}, status: {self.status_code}, detail: {self.detail}"
