from typing import Annotated

from fastapi import Body
from pydantic import BaseModel, EmailStr


class RegisterUserHttpRequest(BaseModel):
    email: Annotated[EmailStr, Body(..., description="User's email")]
    password: Annotated[str, Body(..., description="User's password")]
    first_name: Annotated[str, Body(..., description="User's first name")]
    last_name: Annotated[str, Body(..., description="User's last name")]
    birth_date: Annotated[int, Body(..., description="User's birth date (timestamp)")]
    phone_number: Annotated[str, Body(..., description="User's phone number")]


class LoginUserHttpRequest(BaseModel):
    email: Annotated[EmailStr, Body(..., description="User's email")]
    password: Annotated[str, Body(..., description="User's password", min_length=1)]


class BaseTokenResponse(BaseModel):
    token: str
    expired_at: int


class LoginUserHttpResponse(BaseTokenResponse):
    pass


class RefreshTokenHttpResponse(BaseTokenResponse):
    pass
