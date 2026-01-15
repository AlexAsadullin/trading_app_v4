async def test_register_user(simple_api_client, register_request_body):
    got = await simple_api_client.post(
        "/v1/register",
        json=register_request_body,
    )

    assert got["email"] == register_request_body["email"]
    assert got["name"] == register_request_body["name"]


async def test_register_user_with_existing_email(
    simple_api_client, register_request_body_with_existing_email
):
    got = await simple_api_client.post(
        "/v1/register", json=register_request_body_with_existing_email
    )

    assert got["email"] == register_request_body_with_existing_email["email"]
    assert got["name"] == register_request_body_with_existing_email["name"]


async def test_register_user_with_invalid_email(
    simple_api_client, register_request_body_with_invalid_email
):
    got = await simple_api_client.post(
        "/v1/register",
        json=register_request_body_with_invalid_email,
        expected_status_code=422,
    )

    assert "value is not a valid email address" in got["detail"][0]["msg"]
