import pytest


async def test_login_user_ok(
    simple_api_client, login_request_body, access_token_expired_at
):
    got = await simple_api_client.post(
        "/v1/login",
        json=login_request_body,
        assert_refresh_token=True,
    )

    assert got["token"] is not None
    assert got["expired_at"] >= access_token_expired_at


@pytest.mark.parametrize(
    "email,password",
    [
        ("invalid@test.com", "test"),
        ("test@test.com", "invalid"),
    ],
)
async def test_login_user_not_found(simple_api_client, user, email, password):
    got = await simple_api_client.post(
        "/v1/login",
        json={"email": email, "password": password},
        expected_status_code=404,
    )

    assert got["entity_name"] == "User"
    assert got["entity_id"] == email


@pytest.mark.parametrize(
    "email,password,expected_error_message",
    [
        ("", "test", "value is not a valid email address"),
        (None, "test", "Input should be a valid string"),
        ("test@test.com", None, "Input should be a valid string"),
        ("test@test.com", "", "String should have at least 1 character"),
    ],
)
async def test_login_user_invalid_request(
    simple_api_client, email, password, expected_error_message
):
    got = await simple_api_client.post(
        "/v1/login",
        json={"email": email, "password": password},
        expected_status_code=422,
    )

    assert expected_error_message in got["detail"][0]["msg"]
