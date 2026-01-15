from domain.exceptions import NotFoundError

from ..dtos import UserProfile
from ..mixins import GetUserOrRaiseMixin


class LoginUserCommand(GetUserOrRaiseMixin):
    async def execute(self, email: str, password: str) -> UserProfile:
        user = await self.get_user_or_raise(email=email)
        if not user.verify_password(password):
            raise NotFoundError(entity_name="User", entity_id=email)

        return UserProfile.model_validate(user)
