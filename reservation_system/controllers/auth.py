import asyncio
import random
import string
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from reservation_system.repositories.user import UserRepository
from reservation_system.utils.hashing import check_password, hash_password
from reservation_system.utils.jwt import encode_token
from reservation_system.utils.mail import send_email
from reservation_system.utils.responses import Error, SuccessResponse
from reservation_system.web.api.auth.schema import AuthResponse, RegisterUser, Token, PasswordReset, ForgotPassowrd


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
        refresh_token = encode_token(
            {"id": result.id, "email": result.email, "isAdmin": result.admin},
            expire_days=30,
        )

        await self.repo.create_refresh_token(
            user_id=result.id,
            token=refresh_token,
            expires_at=datetime.now() + timedelta(days=30)
        )
        return AuthResponse(
            status="success",
            message="User created successfully",
            **result.model_dump(exclude_none=True),
            access_token=encode_token(
                {"id": result.id, "email": result.email, "isAdmin": result.admin},
                expire_days=1,
            ),
            refresh_token=refresh_token,
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

        data = {**user.model_dump()}
        refresh_token = encode_token(
            {"id": user.id, "email": user.email, "isAdmin": user.admin}, expire_days=30
        )

        data["access_token"] = encode_token(
            {"id": user.id, "email": user.email, "isAdmin": user.admin}, expire_days=1
        )
        data["refresh_token"] = refresh_token

        await self.repo.create_refresh_token(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now() + timedelta(days=30)
        )

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
        print(token, refresh_token)
        if token != refresh_token:
            raise Error.UNAUTHORIZED

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

        code = "".join(random.choices(string.digits, k=6))

        asyncio.create_task(
            send_email(
                to=data.email,
                subject="Password reset",
                body=f"""
                <p>Here is your password reset code: {code}</p>
                """,
            )
        )

        if not await self.repo.get_by_email(email=data.email):
            raise Error.NOT_FOUND

        await self.repo.add_email_token(
            email=data.email,
            token=code,
            type="reset",
        )
        return SuccessResponse(
            message="Password reset email sent",
        )

    async def reset_password(self, data: PasswordReset):
        """
        Reset password.
        
        :param code: code.
        :param password: password.
        """

        token = await self.repo.get_email_token(code=data.token, type="reset")

        if not token:
            raise Error.NOT_FOUND

        user = await self.repo.get_by_email(email=token.email)

        if not user:
            raise Error.NOT_FOUND

        await self.repo.update(
            user_id=user.id,
            password=hash_password(password=data.password),
        )

        await self.repo.delete_email_token(code=data.token)

        return SuccessResponse(
            message="Password reset successfully",
        )
