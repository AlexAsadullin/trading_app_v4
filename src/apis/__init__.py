from fastapi import APIRouter

from .v1.auth.router import router as auth_router
from .v1.tokens.router import router as tokens_router
from .v1.t_tech_api.router import router as t_tech_router
from .v1.data.router import router as data_router
from .v1.moex_algopack.router import router as moex_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(tokens_router)
v1_router.include_router(t_tech_router)
v1_router.include_router(data_router)
v1_router.include_router(moex_router)


