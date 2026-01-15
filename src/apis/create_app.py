from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

from apis import v1_router
from apis.exceptions import (
    already_exists_error_handler,
    not_found_error_handler,
    unauthorized_error_handler,
)
from config import logger, settings
from dal.engines import get_async_engine
from domain.exceptions import AlreadyExistsError, NotFoundError, UnauthorizedError

TITLE = "Trader Cabinet API"
DESCRIPTION = "API for Trader Cabinet"
CONTACT = {
    "name": "Trader Support",
    "url": "https://bulldogfinance.pro",
    "email": "support@bulldogfinance.pro",
}

VERSION = "1.0.0"

ROOT_PATH = "/api"
DOCS_URL = "/docs"
REDOC_URL = "/redoc"


def create_app() -> FastAPI:
    app = FastAPI(
        title=TITLE,
        description=DESCRIPTION,
        contact=CONTACT,
        root_path=ROOT_PATH,
        version=VERSION,
        debug=settings.debug,
        docs_url=DOCS_URL if settings.debug else None,
        redoc_url=REDOC_URL if settings.debug else None,
    )

    logger.info(f"Starting server {TITLE} [{VERSION}] ...")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=settings.cors_allow_methods,
        allow_headers=["*"],
    )

    app.add_middleware(
        SQLAlchemyMiddleware,
        custom_engine=get_async_engine(),
        session_args={"autoflush": False},
    )

    app.include_router(v1_router)

    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(UnauthorizedError, unauthorized_error_handler)
    app.add_exception_handler(AlreadyExistsError, already_exists_error_handler)

    return app
