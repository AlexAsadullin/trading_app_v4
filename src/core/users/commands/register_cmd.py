from fastapi_async_sqlalchemy import db

from domain.models.users import User

from ..dtos import UserProfile
from ..mixins import GetUserMixin


class RegisterUserCommand(GetUserMixin):
    async def execute(self, email: str, password: str, first_name: str, last_name: str, birth_date: int, phone_number: str) -> UserProfile:
        user = await self.get_user(email=email)
        if user:
            return UserProfile.model_validate(user)

        user = User(email=email, password=password, first_name=first_name, last_name=last_name, birth_date=birth_date, phone_number=phone_number)

        db.session.add(user)
        await db.session.commit()

        return UserProfile.model_validate(user)
