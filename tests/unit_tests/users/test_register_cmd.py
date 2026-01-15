from core.users.commands.register_cmd import RegisterUserCommand


async def test_register_cmd(db_sessions):
    command = RegisterUserCommand()
    got = await command.execute(
        email="test+10@test.com", password="test+10", name="test+10"
    )

    assert got is not None
    assert got.email == "test+10@test.com"
    assert got.name == "test+10"


async def test_register_cmd_with_existing_email(user, db_sessions):
    command = RegisterUserCommand()
    got = await command.execute(email=user.email, password="test+10", name="test+10")

    assert got is not None
    assert got.email == user.email
    assert got.name == user.name
