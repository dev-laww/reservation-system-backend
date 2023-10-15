from typing import Any

from fastapi import HTTPException, status

from ..schemas.response import Response as BaseResponse


class Response:
    """
    Response class.
    """

    @staticmethod
    def ok(message: str, data: Any = None, **kwargs) -> BaseResponse:
        """
        Success response.

        :param message: message.
        :param data: data.
        :param kwargs: additional data.
        :return: SuccessResponse.
        """
        return BaseResponse(
            message=message,
            data=data,
            **kwargs,
        )

    @staticmethod
    def unauthorized(message: str) -> HTTPException:
        """
        Unauthorized response.

        :param message: message.
        :return: Error.
        """
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )

    @staticmethod
    def forbidden(message: str) -> HTTPException:
        """
        Forbidden response.

        :param message: message.
        :return: Error.
        """
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
        )

    @staticmethod
    def not_found(message: str) -> HTTPException:
        """
        Not found response.

        :param message: message.
        :return: Error.
        """
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    @staticmethod
    def bad_request(message: str) -> HTTPException:
        """
        Bad request response.

        :param message: message.
        :return: Error.
        """
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    @staticmethod
    def conflict(message: str) -> HTTPException:
        """
        Conflict response.

        :param message: message.
        :return: Error.
        """
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )
