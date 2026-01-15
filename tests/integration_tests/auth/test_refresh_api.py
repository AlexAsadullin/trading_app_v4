import pytest

from domain.enums import TokenErrorCode, TokenType


async def test_refresh_token_ok(api_client, access_token, access_token_expired_at):
    got = await api_client.post(
        "/v1/refresh",
        assert_refresh_token=True,
    )

    assert got["token"] is not None
    assert got["token"] != access_token
    assert got["expired_at"] >= access_token_expired_at


@pytest.mark.parametrize(
    "existing_refresh_token, expire_days, email, expected_status_code, expected_error_code",
    [
        (None, -1, "test@test.com", 401, TokenErrorCode.expired),
        (None, 10, "invalid@test.com", 401, TokenErrorCode.invalid),
        ("invalid-refresh-token", -1, "test@test.com", 401, TokenErrorCode.invalid),
        ("invalid-refresh-token", 10, "invalid@test.com", 401, TokenErrorCode.invalid),
        (None, 10, None, 401, TokenErrorCode.invalid),
    ],
)
async def test_refresh_token_with_invalid_refresh_token(
    api_client,
    invalid_refresh_token_creator,
    existing_refresh_token,
    expire_days,
    email,
    expected_status_code,
    expected_error_code,
):
    refresh_token = invalid_refresh_token_creator(
        existing_refresh_token, expire_days, email
    )

    got = await api_client.post(
        "/v1/refresh",
        cookies={"refresh_token": refresh_token},
        expected_status_code=expected_status_code,
    )

    assert got["token_type"] == TokenType.refresh_token
    assert got["error_code"] == expected_error_code
