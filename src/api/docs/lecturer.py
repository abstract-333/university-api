from typing import Any

from starlette import status

from api.docs.base import BaseModelException, httpexceptiondict500
from exception.error_code import ErrorModel, ErrorCode
from schemas.auth import AccessRefreshTokens
from schemas.lecturer import LecturerInDB


get_tokens_lecturer_response: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {"model": AccessRefreshTokens},
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
                        "summary": "Lecturer not found",
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
                    ErrorCode.INVALID_REFRESH_TOKEN: {
                        "summary": "Invalid refresh token",
                        "value": {"detail": ErrorCode.INVALID_REFRESH_TOKEN},
                    },
                    ErrorCode.INVALID_DEVICE_ID: {
                        "summary": "Invalid refresh token",
                        "value": {"detail": ErrorCode.INVALID_REFRESH_TOKEN},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
get_me_lecturer_response: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": LecturerInDB,
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
register_lecturer_response: dict[int | str, dict[str, Any]] = {
    status.HTTP_201_CREATED: {
        "model": BaseModelException,
        "content": {
            "application/json": {
                "example": {"message": "success"},
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
                    ErrorCode.USER_NOT_EXISTS: {
                        "summary": "User not found",
                        "value": {"detail": ErrorCode.USER_NOT_EXISTS},
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
                    ErrorCode.INVALID_CREDENTIALS: {
                        "summary": "Entered credentials is invalid",
                        "value": {"detail": ErrorCode.INVALID_CREDENTIALS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}

get_all_my_lecturers_response: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "model": list[LecturerInDB] | None,
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
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
