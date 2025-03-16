from fastapi import Depends
from fastapi.security import APIKeyHeader
from pydantic import SecretStr

from src.backend.config import config
from src.backend.exceptions import UserNotAuthorised

auth = APIKeyHeader(name="access-token")


async def auth_user(token: str = Depends(auth)):
    if SecretStr(token) != config.appconfig.secret_key:
        raise UserNotAuthorised(token)
    return True
