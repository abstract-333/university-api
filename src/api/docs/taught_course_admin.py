from typing import Any

from starlette import status

from api.docs.base import httpexceptiondict500
from exception.error_code import ErrorModel, ErrorCode


add_taught_course_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_201_CREATED: {},
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_NOT_AUTHENTICATED: {
                        "summary": "Not authenticated",
                        "value": {"detail": ErrorCode.USER_NOT_AUTHENTICATED},
                    },
                    ErrorCode.JWT_TOKEN_INVALID: {
                        "summary": "Invalid token",
                        "value": {"detail": ErrorCode.JWT_TOKEN_INVALID},
                    },
                    ErrorCode.EXPIRED_TOKEN: {
                        "summary": "Expired token",
                        "value": {"detail": ErrorCode.EXPIRED_TOKEN},
                    },
                }
            }
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.USER_INACTIVE: {
                        "summary": "User is not active",
                        "value": {"detail": ErrorCode.USER_INACTIVE},
                    },
                    ErrorCode.USER_NOT_VERIFIED: {
                        "summary": "User is not verified",
                        "value": {"detail": ErrorCode.USER_NOT_VERIFIED},
                    },
                    ErrorCode.USER_NOT_ADMIN: {
                        "summary": "User is not superuser",
                        "value": {"detail": ErrorCode.USER_NOT_ADMIN},
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.SPECIALITY_COURSE_NOT_EXISTS: {
                        "summary": "Speciality course is not found",
                        "value": {"detail": ErrorCode.SPECIALITY_COURSE_NOT_EXISTS},
                    },
                }
            }
        },
    },
    status.HTTP_406_NOT_ACCEPTABLE: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.TAUGHT_COURSE_ALREADY_EXISTS: {
                        "summary": "Taught course is already exists",
                        "value": {"detail": ErrorCode.TAUGHT_COURSE_ALREADY_EXISTS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
