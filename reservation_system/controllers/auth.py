from ..repositories import UserRepository
from ..schemas.request import RegisterUser
from ..schemas.response import AuthResponse, Token
from ..utils.hashing import check_password, hash_password
from ..utils.jwt import encode_token
from ..utils.response import Response


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
            raise Response.bad_request(message="Email already exists")

        if data.password != data.password_confirmation:
            raise Response.bad_request(message="Passwords do not match")

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
            raise Response.unauthorized(message="User does not exist")

        if not check_password(password=password, hashed_password=user.password):
            raise Response.unauthorized(message="Incorrect password")

        session = {"id": user.id, "email": user.email, "isAdmin": user.admin}

        data = {
            **user.model_dump(exclude=("password",)),
            "access_token": encode_token(session, expire_days=1),
            "refresh_token": encode_token(session, expire_days=30)
        }

        return Token(
            status="success",
            message="User logged in successfully",
            **data,
        )
