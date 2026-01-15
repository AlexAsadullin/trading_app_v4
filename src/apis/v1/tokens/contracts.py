from typing import Annotated, List

from fastapi import Body
from pydantic import BaseModel

from core.users.dtos import ApiTokenListItemDto


class AddApiTokenHttpRequest(BaseModel):
    platform: Annotated[str, Body(..., description="Platform name")]
    name: Annotated[str, Body(..., description="Token name")]
    token: Annotated[str, Body(..., description="API token")]
    expires_at: Annotated[int, Body(..., description="Expiration timestamp")]


class AddApiTokenHttpResponse(BaseModel):
    id: int
    user_id: int
    platform: str
    name: str
    date_added: int
    expires_at: int


class DeleteApiTokenHttpRequest(BaseModel):
    token_id: Annotated[int, Body(..., description="Token ID to delete")]


class GetAllUserTokensHttpResponse(BaseModel):
    tokens: List[ApiTokenListItemDto]
