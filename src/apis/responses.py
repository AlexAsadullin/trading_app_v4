from pydantic import BaseModel, ConfigDict, Field

from domain.enums import TokenErrorCode, TokenType


class SuccessResponse(BaseModel):
    message: str = Field(..., description="Success message")


class ErrorResponse(BaseModel):
    detail: str


class NotFoundErrorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    entity_name: str = Field(..., description="Entity name")
    entity_id: int = Field(..., description="Entity id")


class AlreadyExistsErrorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    entity_name: str = Field(..., description="Entity name")
    entity_id: str = Field(..., description="Entity id")


class UnauthorizedErrorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token_type: TokenType = Field(..., description="Token type")
    error_code: TokenErrorCode = Field(..., description="Error code")
