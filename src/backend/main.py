import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from pythonjsonlogger import jsonlogger

from src.backend.api.api.v1 import v1_router
from src.backend.config import config
from src.backend.exceptions import BaseAPIException

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(fmt="%(levelname)s %(name)s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


instrumentator = None


# Создаем FastAPI приложение
app = FastAPI(
    title="Investment Optimizer API",
    description="API для оптимизации распределения инвестиций между предприятиями",
    version="1.0.0",
)


@app.exception_handler(BaseAPIException)
async def unicorn_exception_handler(request: Request, exc: BaseAPIException):
    logger.error(str(exc))
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.__repr__()},
    )


instrumentator = Instrumentator().instrument(app)

app.include_router(v1_router, prefix=config.appconfig.api_version_prefix)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "OPTIONS", "HEAD"],
    allow_headers=["*"],
)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(levelname)s %(name)s %(message)s",
        },
        "access": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}

app.mount("/", StaticFiles(directory="src/frontend/", html=True), name="html")
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8080,
        log_config=LOGGING_CONFIG,
    )
