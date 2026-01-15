from fastapi import APIRouter, Depends, Request, Response

from apis.dependencies import get_current_user
from apis.responses import (
    NotFoundErrorResponse,
    SuccessResponse,
    UnauthorizedErrorResponse,
)
from config import settings
from core.users.commands.login_cmd import LoginUserCommand
from core.users.commands.refresh_cmd import RefreshTokenCommand
from core.users.commands.register_cmd import RegisterUserCommand
from core.users.dtos import UserProfile
from domain.enums import TokenType
from domain.services import security

from .contracts import (
    LoginUserHttpRequest,
    LoginUserHttpResponse,
    RefreshTokenHttpResponse,
    RegisterUserHttpRequest,
)

router = APIRouter(prefix="", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserProfile,
)
async def register_user(user: RegisterUserHttpRequest):
    command = RegisterUserCommand()

    return await command.execute(
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        birth_date=user.birth_date,
        phone_number=user.phone_number,
    )


@router.post(
    "/login",
    response_model=LoginUserHttpResponse,
    responses={404: {"model": NotFoundErrorResponse}},
)
async def login_user(response: Response, body: LoginUserHttpRequest):
    command = LoginUserCommand()
    user = await command.execute(email=body.email, password=body.password)

    sub = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
    }
    access_token, access_expired_at = security.create_token(
        sub=sub,
        token_type=TokenType.access_token,
        expire_days=settings.access_token_expire_days,
    )
    refresh_token, refresh_expired_at = security.create_token(
        sub=sub,
        token_type=TokenType.refresh_token,
        expire_days=settings.refresh_token_expire_days,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=refresh_expired_at,
    )

    return LoginUserHttpResponse(
        token=access_token,
        expired_at=access_expired_at,
    )


@router.post(
    "/refresh",
    response_model=RefreshTokenHttpResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
    },
    dependencies=[Depends(get_current_user)],
)
async def refresh_token_endpoint(
    request: Request,
    response: Response,
):
    refresh_token = request.cookies.get("refresh_token")

    command = RefreshTokenCommand()
    result = await command.execute(refresh_token=refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token.token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=result.refresh_token.expired_at,
    )

    return RefreshTokenHttpResponse(
        token=result.access_token.token,
        expired_at=result.access_token.expired_at,
    )


@router.post(
    "/logout",
    response_model=SuccessResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
    },
    dependencies=[Depends(get_current_user)],
)
async def logout(response: Response):
    response.delete_cookie(key="refresh_token")

    return SuccessResponse(message="Successfully logged out")


@router.get(
    "/profile",
    response_model=UserProfile,
    responses={
        401: {"model": UnauthorizedErrorResponse},
    },
)
async def get_profile(user: UserProfile = Depends(get_current_user)):
    return user

