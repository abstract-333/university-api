from typing import Any
from starlette import status
from api.docs.base import httpexceptiondict500, BaseModelException
from exception.error_code import ErrorModel, ErrorCode

accept_pending_lecturer_request_response: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": BaseModelException,
        "content": {
            "application/json": {
                "example": {"message": "request processed"},
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
                        "summary": "User is not admin",
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
                    ErrorCode.LECTURER_REQUEST_NOT_EXISTS: {
                        "summary": "The pending request not found, maybe it has been processed or something went wrong",
                        "value": {"detail": ErrorCode.LECTURER_REQUEST_NOT_EXISTS},
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
                    ErrorCode.LECTURER_ALREADY_REGISTERED: {
                        "summary": "This user is already registered as lecturer in requested faculty",
                        "value": {"detail": ErrorCode.LECTURER_ALREADY_REGISTERED},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
