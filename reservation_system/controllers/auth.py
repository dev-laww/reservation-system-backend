from fastapi import HTTPException, status

from ..repositories import UserRepository
from ..utils.hashing import check_password, hash_password
from ..utils.jwt import encode_token
from ..web.api.auth.schema import AuthResponse, RegisterUser, Token


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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        if data.password != data.password_confirmation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
            )

        mutated = {
            **data.model_dump(exclude=("password_confirmation",)),
            "password": hash_password(password=data.password),
        }

        result = await self.repo.create(**mutated)

        return AuthResponse(
            status="success",
            message="User created successfully",
            **result.model_dump(exclude_none=True),
        )

    async def login(self, email: str, password: str):
        """
        Login user.

        :param email: user email.
        :param password: user password.
        :return: User.
        """
        user = await self.repo.get_by_email(email=email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if not check_password(password=password, hashed_password=user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )

        data = {**user.model_dump(exclude=("password",))}
        data["access_token"] = encode_token(
            {"id": user.id, "email": user.email, "isAdmin": user.admin},
            expire_days=1,
        )
        data["refresh_token"] = encode_token(
            {"id": user.id, "email": user.email, "isAdmin": user.admin},
            expire_days=30,
        )

        return Token(
            status="success",
            message="User logged in successfully",
            **data,
        )
