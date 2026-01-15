from fastapi import APIRouter

from .v1.auth.router import router as auth_router
from .v1.tokens.router import router as tokens_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(tokens_router)


