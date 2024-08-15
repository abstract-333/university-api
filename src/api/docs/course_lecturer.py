from typing import Any

from starlette import status

from api.docs.base import httpexceptiondict500
from exception.error_code import ErrorModel, ErrorCode
from schemas.course_lecturer import CourseLecturerInDBExtended
from schemas.taught_course import TaughtCourseUpdate

get_courses_me_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": list[CourseLecturerInDBExtended] | None,
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

join_existing_course_responses: dict[int | str, dict[str, Any]] = {
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
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.LECTURER_NOT_EXISTS: {
                        "summary": "Lecturer is not found",
                        "value": {"detail": ErrorCode.LECTURER_NOT_EXISTS},
                    },
                    ErrorCode.TAUGHT_COURSE_NOT_EXISTS: {
                        "summary": "Taught course is not found",
                        "value": {"detail": ErrorCode.TAUGHT_COURSE_NOT_EXISTS},
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
                    ErrorCode.COURSE_LECTURER_ALREADY_EXISTS: {
                        "summary": "Course lecturer is already exists",
                        "value": {"detail": ErrorCode.COURSE_LECTURER_ALREADY_EXISTS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
add_course_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_201_CREATED: {},
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.FORBIDDEN: {
                        "summary": "Error while adding to db",
                        "value": {"detail": ErrorCode.FORBIDDEN},
                    },
                }
            }
        },
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
edit_course_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": TaughtCourseUpdate,
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
    status.HTTP_406_NOT_ACCEPTABLE: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.LECTURER_NOT_TEACHING_COURSE: {
                        "summary": "User must be the lecturer of course to be eligible to edit it",
                        "value": {"detail": ErrorCode.LECTURER_NOT_TEACHING_COURSE},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
