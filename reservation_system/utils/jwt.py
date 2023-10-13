from jose import jwt, JWTError
from fastapi import HTTPException, status

from reservation_system.settings import settings


def encode_token(data: dict) -> str:
    """
    Encodes a jwt token.

    :param data: data to encode.
    :return: jwt token.
    """
    return jwt.encode(data, key=settings.jwt_secret, algorithm="HS256")


def decode_token(token: str) -> dict:
    """
    Decodes a jwt token.

    :param token: jwt token.
    :return: decoded token.
    :raises HTTPException: if token is invalid.
    """
    try:
        return jwt.decode(token, key=settings.jwt_secret, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
