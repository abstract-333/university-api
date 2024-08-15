from datetime import datetime, timedelta, timezone
from typing import Any, Mapping
from jose import ExpiredSignatureError
import jwt
from exception.base import ExceptionUnauthorized401
from exception.error_code import ErrorCode
from settings import settings_obj


class JWTManager:
    @staticmethod
    def _encode_token(payload: dict) -> bytes:
        jwt_token: bytes = jwt.encode(
            payload=payload,
            key=settings_obj.JWT_SECRET_KEY,
            algorithm=settings_obj.JWT_ALGORITHM,
        )
        return jwt_token

    @staticmethod
    def decode_token(token: str) -> Mapping[Any, Any]:
        try:
            payload: Mapping[Any, Any] = jwt.decode(
                jwt=token,
                key=settings_obj.JWT_SECRET_KEY,
                algorithms=[settings_obj.JWT_ALGORITHM],
            )
            return payload

        except ExpiredSignatureError:
            raise ExceptionUnauthorized401(detail=ErrorCode.EXPIRED_TOKEN)

        except Exception:
            raise ExceptionUnauthorized401(detail=ErrorCode.JWT_TOKEN_INVALID)

    @staticmethod
    def create_jwt_token(
        valid_duration: int,
        **other: dict,
    ) -> bytes:
        now: datetime = datetime.now(tz=timezone.utc)
        payload: dict = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=valid_duration),
            **other,
        }

        jwt_token: bytes = JWTManager._encode_token(
            payload=payload,
        )

        return jwt_token

    @staticmethod
    def extract_from_payload(payload: Mapping, key: str) -> Any | None:
        return payload.get(key)
