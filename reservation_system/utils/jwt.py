from datetime import datetime, timedelta

from jose import jwt, JWTError
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer

from reservation_system.settings import settings
from reservation_system.utils.responses import Error
from reservation_system.schemas.token import JWTData


def encode_token(data: dict, expire_days: int = 1) -> str:
    """
    Encodes a jwt token.

    :param data: data to encode.
    :return: jwt token.
    """
    expiry = datetime.now() + timedelta(days=expire_days)
    data["exp"] = int(expiry.timestamp())

    return jwt.encode(data, key=settings.jwt_secret, algorithm="HS256")


def decode_token(token: str) -> dict:
    """
    Decodes a jwt token.

    :param token: jwt token.
    :return: decoded token.
    :raises HTTPException: if token is invalid.
    """
    try:
        decoded = jwt.decode(token, key=settings.jwt_secret, algorithms=["HS256"])

        if decoded["exp"] < datetime.now().timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return decoded


class TokenBearer(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=False)

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)

        if not credentials or not credentials.scheme == "Bearer":
            raise Error.unauthorized

        return self.verify_jwt(credentials.credentials)

    def verify_jwt(self, token: str):
        return JWTData(**decode_token(token))


class AdminTokenBearer(TokenBearer):
    def verify_jwt(self, token: str):
        return super().verify_jwt(token).is_admin


AUTH = TokenBearer()  # authorization dependency
ADMIN_AUTH = AdminTokenBearer()  # admin authorization dependency
