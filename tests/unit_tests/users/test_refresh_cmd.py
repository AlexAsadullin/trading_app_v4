import pytest

from config import current_ts, settings
from core.users.commands.refresh_cmd import RefreshTokenCommand
from domain.enums import TokenErrorCode, TokenType
from domain.exceptions import UnauthorizedError


async def test_refresh_cmd_ok(refresh_token_data, db_sessions):
    command = RefreshTokenCommand()
    got = await command.execute(refresh_token=refresh_token_data.token)

    assert got is not None
    assert got.access_token is not None
    assert got.refresh_token is not None
    assert (
        got.refresh_token.expired_at
        > current_ts() + settings.refresh_token_expire_days * 24 * 60 * 60 * 1000
    )


@pytest.mark.parametrize("refresh_token", ["", None, "invalid"])
async def test_refresh_cmd_with_invalid_refresh_token(db_sessions, refresh_token):
    command = RefreshTokenCommand()
    with pytest.raises(UnauthorizedError) as exc_info:
        await command.execute(refresh_token=refresh_token)

    assert exc_info.value is not None
    assert exc_info.value.token_type == TokenType.refresh_token
    assert exc_info.value.error_code == TokenErrorCode.invalid


async def test_refresh_cmd_with_expired_refresh_token(
    expired_refresh_token_data, db_sessions
):
    command = RefreshTokenCommand()
    with pytest.raises(UnauthorizedError) as exc_info:
        await command.execute(refresh_token=expired_refresh_token_data.token)

    assert exc_info.value is not None
    assert exc_info.value.token_type == TokenType.refresh_token
    assert exc_info.value.error_code == TokenErrorCode.expired
