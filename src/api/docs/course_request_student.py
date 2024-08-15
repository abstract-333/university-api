from typing import Any

from starlette import status

from api.docs.base import httpexceptiondict500
from exception.error_code import ErrorModel, ErrorCode
from schemas.course_request import CourseRequestInDBExtended

send_course_request_responses: dict[int | str, dict[str, Any]] = {
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
                }
            }
        },
    },
    status.HTTP_406_NOT_ACCEPTABLE: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.STUDENT_ALREADY_ENROLLED_IN_COURSE: {
                        "summary": "Student is already registered in course",
                        "value": {
                            "detail": ErrorCode.STUDENT_ALREADY_ENROLLED_IN_COURSE
                        },
                        ErrorCode.COURSE_REQUEST_ALREADY_SENT: {
                            "summary": "Request to join course  is already sent",
                            "value": {"detail": ErrorCode.COURSE_REQUEST_ALREADY_SENT},
                        },
                    }
                }
            },
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}

get_pending_requests_response: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": list[CourseRequestInDBExtended] | None,
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


update_course_request_response: dict[int | str, dict[str, Any]] = {
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
                    ErrorCode.COURSE_REQUEST_NOT_EXISTS: {
                        "summary": "The pending request not found, maybe it has been processed or something went wrong",
                        "value": {"detail": ErrorCode.COURSE_REQUEST_NOT_EXISTS},
                    },
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
