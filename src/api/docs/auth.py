from typing import Any

from starlette import status

from exception.error_code import ErrorModel, ErrorCode
from schemas.auth import AccessRefreshTokens
from .base import httpexceptiondict500
from settings.settings import settings_obj

sign_in_response: dict[int | str, dict[str, Any]] = {
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
                    ErrorCode.LOGIN_BAD_CREDENTIALS: {
                        "summary": "Invalid credentials",
                        "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
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
                    ErrorCode.SESSION_ALREADY_EXISTS: {
                        "summary": "Session already exists in this device",
                        "value": {"detail": ErrorCode.SESSION_ALREADY_EXISTS},
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
                    ErrorCode.LOGIN_BAD_CREDENTIALS: {
                        "summary": "Incorrect email or password",
                        "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
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
                    ErrorCode.TOO_MANY_SESSIONS: {
                        "summary": f"User can't have more than {settings_obj.SESSIONS_NUMBER} sessions",
                        "value": {"detail": ErrorCode.TOO_MANY_SESSIONS},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
get_tokens_response: dict[int | str, dict[str, Any]] = {
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
sign_out_response: dict[int | str, dict[str, Any]] = {
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
                    ErrorCode.INVALID_REFRESH_TOKEN: {
                        "summary": "Invalid refresh token",
                        "value": {"detail": ErrorCode.INVALID_REFRESH_TOKEN},
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: httpexceptiondict500,
}
