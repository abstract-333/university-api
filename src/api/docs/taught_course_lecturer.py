from typing import Any

from starlette import status

from api.docs.base import httpexceptiondict500
from exception.error_code import ErrorModel, ErrorCode
from schemas.taught_course import TaughtCourseInDBExtended

get_taught_courses_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": list[TaughtCourseInDBExtended] | None,
    },
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
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.LECTURER_NOT_EXISTS: {
                        "summary": "Lecturer is not found",
                        "value": {"detail": ErrorCode.LECTURER_NOT_EXISTS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}

get_taught_course_by_speciality_course_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": TaughtCourseInDBExtended | None,
    },
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
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.LECTURER_NOT_EXISTS: {
                        "summary": "Lecturer is not found",
                        "value": {"detail": ErrorCode.LECTURER_NOT_EXISTS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
get_taught_courses_in_faculty_now_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": list[TaughtCourseInDBExtended] | None,
    },
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
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.LECTURER_NOT_EXISTS: {
                        "summary": "Lecturer is not found",
                        "value": {"detail": ErrorCode.LECTURER_NOT_EXISTS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
