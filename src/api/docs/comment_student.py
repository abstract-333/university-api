from typing import Any

from starlette import status

from api.docs.base import httpexceptiondict500
from exception.error_code import ErrorModel, ErrorCode
from schemas.comment import CommentInDBExtended

get_comments_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": list[CommentInDBExtended] | None,
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
                        "summary": "Student is not registered in course",
                        "value": {"detail": ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
add_comment_responses: dict[int | str, dict[str, Any]] = {
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
                        "summary": "Student is not registered in course",
                        "value": {"detail": ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE},
                    },
                    ErrorCode.POST_NOT_FOUND: {
                        "summary": "Post is not found",
                        "value": {"detail": ErrorCode.POST_NOT_FOUND},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}

update_comment_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_202_ACCEPTED: {},
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
                    ErrorCode.COMMENT_NOT_FOUND: {
                        "summary": "Comment is not found",
                        "value": {"detail": ErrorCode.COMMENT_NOT_FOUND},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}


delete_comment_responses: dict[int | str, dict[str, Any]] = {
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
                    ErrorCode.STUDENT_NOT_EXISTS: {
                        "summary": "Student is not found",
                        "value": {"detail": ErrorCode.STUDENT_NOT_EXISTS},
                    },
                    ErrorCode.COMMENT_NOT_FOUND: {
                        "summary": "Comment is not found",
                        "value": {"detail": ErrorCode.COMMENT_NOT_FOUND},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
