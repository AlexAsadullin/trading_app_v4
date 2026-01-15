import pytest

from core.users.commands.login_cmd import LoginUserCommand
from domain.exceptions import NotFoundError


async def test_login_cmd(user, db_sessions):
    command = LoginUserCommand()
    got = await command.execute(email=user.email, password="test")

    assert got is not None
    assert got.email == user.email
    assert got.name == user.name


@pytest.mark.parametrize("password", ["invalid", "1234567890"])
async def test_login_cmd_with_invalid_password(user, db_sessions, password):
    command = LoginUserCommand()
    with pytest.raises(NotFoundError) as exc_info:
        await command.execute(email=user.email, password=password)

    assert exc_info.value is not None
    assert exc_info.value.entity_name == "User"
    assert exc_info.value.entity_id == user.email


@pytest.mark.parametrize("email", ["invalid@test.com", "1234567890"])
async def test_login_cmd_with_invalid_email(db_sessions, email):
    command = LoginUserCommand()
    with pytest.raises(NotFoundError) as exc_info:
        await command.execute(email=email, password="test")

    assert exc_info.value is not None
    assert exc_info.value.entity_name == "User"
    assert exc_info.value.entity_id == email
