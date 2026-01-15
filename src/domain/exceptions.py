from domain.enums import TokenErrorCode, TokenType


class BaseError(Exception):
    entity_name: str
    entity_id: int | str

    def __init__(self, entity_name: str, entity_id: int | str):
        self.entity_name = entity_name
        self.entity_id = entity_id


class NotFoundError(BaseError):
    def __str__(self):
        return f"{self.entity_name} with id {self.entity_id} not found"


class AlreadyExistsError(BaseError):
    def __str__(self):
        return f"{self.entity_name} with {self.entity_id} already exists"


class UnauthorizedError(BaseError):
    error_code: TokenErrorCode
    token_type: TokenType

    def __init__(self, token_type: TokenType, error_code: TokenErrorCode):
        self.token_type = token_type
        self.error_code = error_code

    @classmethod
    def token_expired(
        cls,
        token_type: TokenType,
    ) -> "UnauthorizedError":
        return cls(
            token_type=token_type,
            error_code=TokenErrorCode.expired,
        )

    @classmethod
    def invalid_token(
        cls,
        token_type: TokenType,
    ) -> "UnauthorizedError":
        return cls(
            token_type=token_type,
            error_code=TokenErrorCode.invalid,
        )
