from typing import Any

from starlette import status

from api.docs.base import httpexceptiondict500
from exception.error_code import ErrorModel, ErrorCode
from schemas.quiz import QuizInDBExtended

get_quizzes_course_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": list[QuizInDBExtended] | None,
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
                    ErrorCode.LECTURER_NOT_TEACHING_COURSE: {
                        "summary": "Course Lecturer raw not exist",
                        "value": {"detail": ErrorCode.LECTURER_NOT_TEACHING_COURSE},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}

add_quiz_responses: dict[int | str, dict[str, Any]] = {
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
                    ErrorCode.LECTURER_NOT_TEACHING_COURSE: {
                        "summary": "Course Lecturer raw not exist",
                        "value": {"detail": ErrorCode.LECTURER_NOT_TEACHING_COURSE},
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
                    ErrorCode.NOT_ENOUGH_QUESTIONS: {
                        "summary": "Not enough questions to make quiz",
                        "value": {"detail": ErrorCode.NOT_ENOUGH_QUESTIONS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
delete_quiz_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_204_NO_CONTENT: {},
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
                    ErrorCode.LECTURER_NOT_TEACHING_COURSE: {
                        "summary": "Course Lecturer raw not exist",
                        "value": {"detail": ErrorCode.LECTURER_NOT_TEACHING_COURSE},
                    },
                    ErrorCode.QUIZ_NOT_EXISTS: {
                        "summary": "Quiz is not found",
                        "value": {"detail": ErrorCode.QUIZ_NOT_EXISTS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
