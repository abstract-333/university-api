from typing import Any

from starlette import status

from api.docs.base import httpexceptiondict500
from exception.error_code import ErrorModel, ErrorCode
from schemas.quiz_result import QuizResultInDB


add_quiz_result_responses: dict[int | str, dict[str, Any]] = {
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
                    ErrorCode.STUDENT_NOT_EXISTS: {
                        "summary": "Student is not found",
                        "value": {"detail": ErrorCode.STUDENT_NOT_EXISTS},
                    },
                    ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE: {
                        "summary": "Student is not enrolled in course",
                        "value": {"detail": ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE},
                    },
                    ErrorCode.QUIZ_NOT_EXISTS: {
                        "summary": "Quiz is not found",
                        "value": {"detail": ErrorCode.QUIZ_NOT_EXISTS},
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
                    ErrorCode.RESULT_GREATER_THAN_QUIZ_MARKS: {
                        "summary": "Entered result is greater than max mark in quiz",
                        "value": {"detail": ErrorCode.RESULT_GREATER_THAN_QUIZ_MARKS},
                    },
                    ErrorCode.QUIZ_RESULT_ALREADY_EXISTS: {
                        "summary": "Quiz result is already exists",
                        "value": {"detail": ErrorCode.QUIZ_RESULT_ALREADY_EXISTS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}

get_quizzes_results_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": list[QuizResultInDB] | None,
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
                    ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE: {
                        "summary": "Student is not enrolled in course",
                        "value": {"detail": ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
