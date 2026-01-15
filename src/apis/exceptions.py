from fastapi import Request
from fastapi.responses import JSONResponse

from domain.exceptions import AlreadyExistsError, NotFoundError, UnauthorizedError


async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"entity_name": exc.entity_name, "entity_id": exc.entity_id},
    )


async def unauthorized_error_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=401,
        content={"token_type": exc.token_type, "error_code": exc.error_code},
    )


async def already_exists_error_handler(request: Request, exc: AlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={"entity_name": exc.entity_name, "entity_id": exc.entity_id},
    )
