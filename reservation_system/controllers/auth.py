from fastapi import HTTPException, status

from reservation_system.repositories.user import UserRepository
from reservation_system.web.api.auth.schema import RegisterUser


class AuthController:
    repo = UserRepository()

    async def register(self, data: RegisterUser):
        """
        Register user.

        :param data: user data.
        :return: User.
        """
        user = await self.repo.get_by_email(email=data.email)

        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        if data.password != data.password_confirmation:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

        return await self.repo.create(**data.model_dump(exclude=["password_confirmation"]))
