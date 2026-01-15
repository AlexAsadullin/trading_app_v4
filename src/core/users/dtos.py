from pydantic import BaseModel, ConfigDict


class TokenData(BaseModel):
    token: str
    expired_at: int


class RefreshTokenDto(BaseModel):
    access_token: TokenData
    refresh_token: TokenData


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    first_name: str
    last_name: str
    birth_date: int
    phone_number: str
    register_date: int
