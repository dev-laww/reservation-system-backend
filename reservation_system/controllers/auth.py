import asyncio
import random
import string

from ..repositories import UserRepository
from ..schemas.request import ForgotPassowrd, PasswordReset, RegisterUser
from ..schemas.response import AuthResponse, Token
from ..utils.hashing import check_password, hash_password
from ..utils.jwt import encode_token
from ..utils.mail import send_email
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
            "refresh_token": encode_token(session, expire_days=30),
        }

        return Token(
            status="success",
            message="User logged in successfully",
            **data,
        )

    async def refresh_token(self, user_id: int, refresh_token: str):
        """
        Refresh an access token.

        :param refresh_token: refresh token.
        :return: new access token.
        """
        token = await self.repo.get_refresh_token(user_id=user_id)

        if token != refresh_token:
            raise Response.bad_request(message="Invalid refresh token")

        user = await self.repo.get_by_id(user_id=user_id)
        data = {
            "access_token": encode_token(
                {"id": user.id, "email": user.email, "isAdmin": user.admin},
                expire_days=1,
            ),
        }

        return Token(
            status="success",
            message="Token refreshed",
            **data,
        )

    async def forgot_password(self, data: ForgotPassowrd):
        """
        Forgot password.

        :param email: email.
        """

        token = "".join(random.choices([*string.digits, *string.ascii_letters], k=20))

        asyncio.create_task(
            send_email(
                to=data.email,
                subject="Password reset",
                body=f"""
                <a>http://localhost:3000/auth/reset-password?token={token}</a>
                """,
            )
        )

        if not await self.repo.get_by_email(email=data.email):
            raise Response.not_found(message="User not found")

        await self.repo.add_email_token(
            email=data.email,
            token=token,
            type="reset",
        )
        return Response.ok(message="Password reset email sent")

    async def reset_password(self, data: PasswordReset):
        """
        Reset password.

        :param code: code.
        :param password: password.
        """

        token = await self.repo.get_email_token(code=data.token, type="reset")

        if not token:
            raise Response.bad_request(message="Invalid token")

        user = await self.repo.get_by_email(email=token.email)

        if not user:
            raise Response.not_found(message="User not found")

        await self.repo.update(
            user_id=user.id,
            password=hash_password(password=data.password),
        )

        await self.repo.delete_email_token(code=data.token)

        return Response.ok(message="Password reset successfully")
