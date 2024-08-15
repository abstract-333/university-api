from typing import Any

from starlette import status

from api.docs.base import httpexceptiondict500
from exception.error_code import ErrorModel, ErrorCode
from schemas.speciality_course import SpecialityCourseInDB

get_speciality_courses_for_my_speciality_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": list[SpecialityCourseInDB] | None,
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
                    ErrorCode.STUDENT_NOT_EXISTS: {
                        "summary": "Student is not found",
                        "value": {"detail": ErrorCode.STUDENT_NOT_EXISTS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
