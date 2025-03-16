from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from src.backned.api.endpoints import upload_file

v1_router = APIRouter()

v1_router.include_router(
    upload_file.router,
    prefix="/files",
    tags=["files"],
)


@v1_router.get("/redirect_dl", include_in_schema=False)
def redirect_deep_link(url: str):
    return RedirectResponse(url)
