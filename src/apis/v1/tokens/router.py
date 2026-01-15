from fastapi import APIRouter, Depends

from apis.dependencies import get_current_user
from apis.responses import (
    NotFoundErrorResponse,
    SuccessResponse,
    UnauthorizedErrorResponse,
)
from core.users.commands.add_api_token_cmd import AddApiTokenCommand
from core.users.commands.delete_api_token_cmd import DeleteApiTokenCommand
from core.users.dtos import UserProfile
from core.users.queries.get_all_user_tokens_query import GetAllUserTokensQuery

from .contracts import (
    AddApiTokenHttpRequest,
    AddApiTokenHttpResponse,
    DeleteApiTokenHttpRequest,
    GetAllUserTokensHttpResponse,
)

router = APIRouter(prefix="", tags=["Tokens"])


@router.post(
    "/tokens",
    response_model=AddApiTokenHttpResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
    },
)
async def add_api_token(
    body: AddApiTokenHttpRequest,
    user: UserProfile = Depends(get_current_user),
):
    command = AddApiTokenCommand()
    return await command.execute(
        user_id=user.id,
        platform=body.platform,
        name=body.name,
        token=body.token,
        expires_at=body.expires_at,
    )


@router.delete(
    "/tokens/{token_id}",
    response_model=SuccessResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
    },
)
async def delete_api_token(
    token_id: int,
    user: UserProfile = Depends(get_current_user),
):
    command = DeleteApiTokenCommand()
    await command.execute(token_id=token_id, user_id=user.id)
    return SuccessResponse(message="Token deleted successfully")


@router.get(
    "/tokens",
    response_model=GetAllUserTokensHttpResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
    },
)
async def get_all_user_tokens(
    user: UserProfile = Depends(get_current_user),
):
    query = GetAllUserTokensQuery()
    tokens = await query.execute(user_id=user.id)
    return GetAllUserTokensHttpResponse(tokens=tokens)
