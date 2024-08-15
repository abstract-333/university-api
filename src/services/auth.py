import base64
import hashlib
import time
from typing import Mapping
import uuid

from argon2 import PasswordHasher
from fastapi import Depends
from fastapi.security import (
    OAuth2PasswordBearer,
)
from pydantic import EmailStr, ValidationError

from common import IUnitOfWork
from common.jwt import JWTManager
from exception import (
    ExceptionNotAcceptable406,
    ExceptionNotFound404,
    ExceptionForbidden403,
    ExceptionUnauthorized401,
)
from exception.error_code import ErrorCode
from schemas import (
    UserRead,
    AccessRefreshTokens,
    UserCreate,
    UserHashedPassword,
    UserReadWithPassword,
)
from schemas.active_session import (
    ActiveSessionCreate,
    ActiveSessionInDB,
    ActiveSessionUpdate,
)
from schemas.pagination import Pagination
from settings import settings_obj
from specification.active_session import (
    SessionDeviceIdSpecification,
    SessionIdSpecification,
    SessionRefreshTokenSpecification,
    SessionUserIdSpecification,
)
from specification.user import UserEmailSpecification, UserIdSpecification

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in", scheme_name="User")


class AuthService:
    def __init__(
        self,
        is_superuser: bool | None = None,
        is_verified: bool | None = None,
        is_active: bool | None = None,
    ) -> None:
        self.is_verified: bool | None = is_verified
        self.is_active: bool | None = is_active
        self.is_superuser: bool | None = is_superuser
        self.password_hasher = PasswordHasher(
            hash_len=32, salt_len=16, memory_cost=65536 // 2
        )

    async def get_current_user(
        self,
        token: str = Depends(dependency=oauth2_scheme),
    ) -> UserRead:
        current_user: UserRead = await self.validate_access_token(token=token)
        await self.check_user_state(current_user=current_user)
        return current_user

    @classmethod
    async def _get_user_by_email(
        cls,
        uow: IUnitOfWork,
        email: EmailStr,
    ) -> UserReadWithPassword | None:
        async with uow:
            user: UserReadWithPassword | None = await uow.user.get_user(
                specification=UserEmailSpecification(email=email)
            )
            return user

    @classmethod
    async def _get_user_by_id(
        cls,
        uow: IUnitOfWork,
        id: uuid.UUID,
    ) -> UserReadWithPassword | None:
        async with uow:
            user: UserReadWithPassword | None = await uow.user.get_user(
                specification=UserIdSpecification(id=id)
            )
            return user

    @classmethod
    async def _add_user(
        cls,
        uow: IUnitOfWork,
        user_data: dict,
    ) -> None:
        """Add user to users table"""
        async with uow:
            await uow.user.add_user(user_data=user_data)
            await uow.commit()

    @classmethod
    async def _get_sessions_by_user(
        cls,
        user_id: uuid.UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[ActiveSessionInDB] | None:
        """Get active sessions by user_id"""
        async with uow:
            active_sessions: list[
                ActiveSessionInDB
            ] | None = await uow.active_session.get_sessions(
                pagination=pagination,
                specification=SessionUserIdSpecification(user_id=user_id),
            )
            return active_sessions

    @classmethod
    async def _get_session_by_device_and_user(
        cls,
        user_id: uuid.UUID,
        device_id: str,
        uow: IUnitOfWork,
    ) -> ActiveSessionInDB | None:
        """Get active session by user_id and device_id"""
        async with uow:
            active_session: ActiveSessionInDB | None = (
                await uow.active_session.get_session(
                    specification=SessionUserIdSpecification(user_id=user_id)
                    & SessionDeviceIdSpecification(device_id=device_id),
                )
            )
            return active_session

    @classmethod
    async def _get_session_by_user_and_token(
        cls,
        user_id: uuid.UUID,
        refresh_token: str,
        uow: IUnitOfWork,
    ) -> ActiveSessionInDB | None:
        """Get active session by user_id and refresh_token"""
        async with uow:
            active_session: ActiveSessionInDB | None = (
                await uow.active_session.get_session(
                    specification=SessionUserIdSpecification(user_id=user_id)
                    & SessionRefreshTokenSpecification(refresh_token=refresh_token),
                )
            )
            return active_session

    @classmethod
    async def _add_session(
        cls,
        session_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        """Add session"""
        async with uow:
            await uow.active_session.add_session(session_data=session_data)
            await uow.commit()

    @classmethod
    async def _edit_session_by_id(
        cls,
        session_data: dict,
        session_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        """Edit session by session_id"""
        async with uow:
            await uow.active_session.edit_session(
                session_edit=session_data,
                specification=SessionIdSpecification(session_id=session_id),
            )
            await uow.commit()

    @classmethod
    async def _delete_session_by_session_id(
        cls,
        session_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        """Delete session by session_id"""
        async with uow:
            await uow.active_session.delete_session(
                specification=SessionIdSpecification(session_id=session_id)
            )
            await uow.commit()

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hasher.verify(
            password=plain_password, hash=hashed_password
        )

    async def hash_password(self, password: str) -> str:
        return self.password_hasher.hash(password=password)

    async def get_user_from_payload(
        self,
        payload: Mapping,
    ) -> UserRead:
        exception = ExceptionUnauthorized401(
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )
        user_data: Mapping[str, str] | None = JWTManager.extract_from_payload(
            payload=payload, key="user"
        )
        if user_data is None:
            # TODO Make Exception
            raise ValidationError()
        try:
            user = UserRead(**user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    async def _create_jwt_access_token(cls, user: UserRead) -> bytes:
        jwt_token: bytes = JWTManager.create_jwt_token(
            valid_duration=settings_obj.JWT_EXPIRATION_ACCESS_TOKEN,
            user=user.model_dump(mode="json"),
        )
        return jwt_token

    async def validate_access_token(self, token: str) -> UserRead:
        payload: Mapping = JWTManager.decode_token(token=token)
        user: UserRead = await self.get_user_from_payload(payload=payload)

        return user

    @classmethod
    async def _create_jwt_refresh_token(
        cls,
        user_id: uuid.UUID,
    ) -> bytes:
        jwt_token: bytes = JWTManager.create_jwt_token(
            valid_duration=settings_obj.JWT_EXPIRATION_REFRESH_TOKEN,
            sub=str(object=user_id),
        )
        return jwt_token

    async def register_new_user(
        self,
        user_data: UserCreate,
        uow: IUnitOfWork,
    ) -> bool:
        exception_email = ExceptionNotAcceptable406(
            detail=ErrorCode.EMAIL_ALREADY_EXISTS
        )

        # Check that email is not already taken
        user_with_same_email: UserReadWithPassword | None = (
            await self._get_user_by_email(email=user_data.email, uow=uow)
        )
        if user_with_same_email is not None:
            raise exception_email

        hashed_password: str = await self.hash_password(password=user_data.password)
        user = UserHashedPassword(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=False,
            is_superuser=False,
        )
        await self._add_user(
            user_data=user.model_dump(
                exclude={"is_active", "is_verified", "is_superuser"}
            ),
            uow=uow,
        )

        return True

    @classmethod
    def _hash_text(cls, text_for_hashing: str) -> str:
        hashed_text = hashlib.sha256(string=text_for_hashing.encode())
        hashed_bytes: bytes = hashed_text.digest()
        hashed_string: str = base64.b64encode(hashed_bytes).decode()
        return hashed_string

    @classmethod
    def _get_expire_time_refresh_token(cls) -> int:
        return int(time.time()) + settings_obj.JWT_EXPIRATION_REFRESH_TOKEN

    async def _validate_session(
        self,
        sessions: list[ActiveSessionInDB],
        device_id: str,
    ) -> None | str:
        for session in sessions:
            if session.device_id == device_id and session.expire_at < int(time.time()):
                return session.device_id

    async def _create_session(
        self,
        device_id: str,
        device_name: str,
        user_id: uuid.UUID,
        expire_time: int,
        refresh_token: str,
        uow: IUnitOfWork,
    ) -> None:
        """Create session using device_id, user_id, expire_time, refresh_token arguments"""

        session_for_db = ActiveSessionCreate(
            device_id=device_id,
            user_id=user_id,
            expire_at=expire_time,
            device_name=device_name,
            refresh_token=refresh_token,
        )
        await self._add_session(session_data=session_for_db.model_dump(), uow=uow)

    async def _update_session_by_id(
        self,
        expire_time: int,
        refresh_token: str,
        session_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        """Update session attributes(expire_time, refresh_token) using session_id"""

        updated_session = ActiveSessionUpdate(
            expire_at=expire_time,
            refresh_token=refresh_token,
        )
        await self._edit_session_by_id(
            session_data=updated_session.model_dump(),
            session_id=session_id,
            uow=uow,
        )

    async def _authenticate_user(
        self,
        email: str,
        password: str,
        uow: IUnitOfWork,
    ) -> UserReadWithPassword:
        try:
            user: UserReadWithPassword | None = await self._get_user_by_email(
                email=email,
                uow=uow,
            )

            if not user:
                raise ExceptionNotFound404(detail=ErrorCode.LOGIN_BAD_CREDENTIALS)

            await self.verify_password(
                plain_password=password,
                hashed_password=user.hashed_password,
            )

            await self.check_user_state(current_user=user)

            return user
        except Exception as exception:
            raise exception

    async def authenticate_user_using_device_id(
        self,
        email: str,
        password: str,
        device_id: str,
        device_name: str,
        uow: IUnitOfWork,
    ) -> AccessRefreshTokens:
        try:
            user: UserReadWithPassword = await self._authenticate_user(
                email=email, password=password, uow=uow
            )
            sessions: list[ActiveSessionInDB] | None = await self._get_sessions_by_user(
                user_id=user.id, pagination=Pagination(), uow=uow
            )

            token: AccessRefreshTokens = await self.generate_access_refresh_tokens(
                user=user
            )
            expire_time: int = self._get_expire_time_refresh_token()
            hashed_device_id: str = self._hash_text(text_for_hashing=device_id)
            refresh_token: str = str(object=token.refresh_token, encoding="utf-8")

            # Add new session, if there is no sessions
            if sessions is None:
                await self._create_session(
                    device_id=hashed_device_id,
                    device_name=device_name,
                    user_id=user.id,
                    expire_time=expire_time,
                    refresh_token=refresh_token,
                    uow=uow,
                )
                return token

            # Check if number of session didn't exceed valid number
            if len(sessions) >= settings_obj.SESSIONS_NUMBER:
                raise ExceptionNotAcceptable406(detail=ErrorCode.TOO_MANY_SESSIONS)

            # Check if session with same device_id didn't exists
            for session in sessions:
                if session.device_id == hashed_device_id:
                    raise ExceptionForbidden403(detail=ErrorCode.SESSION_ALREADY_EXISTS)

            # Add new session in other cases
            else:
                await self._create_session(
                    device_id=hashed_device_id,
                    user_id=user.id,
                    expire_time=expire_time,
                    device_name=device_name,
                    refresh_token=refresh_token,
                    uow=uow,
                )

            return token

        except Exception as exception:
            raise exception

    async def authenticate_user(
        self,
        email: str,
        password: str,
        uow: IUnitOfWork,
    ) -> AccessRefreshTokens:
        try:
            user: UserReadWithPassword = await self._authenticate_user(
                email=email, password=password, uow=uow
            )
            await self.check_user_state(current_user=user)
            token: AccessRefreshTokens = await self.generate_access_refresh_tokens(
                user=user
            )

            return token

        except Exception as exception:
            raise exception

    async def generate_access_refresh_tokens(
        self,
        user: UserRead,
    ) -> AccessRefreshTokens:
        access_token: bytes = await self._create_jwt_access_token(user=user)
        refresh_token: bytes = await self._create_jwt_refresh_token(user_id=user.id)
        return AccessRefreshTokens(
            access_token=access_token, refresh_token=refresh_token
        )

    async def check_user_state(
        self,
        current_user: UserRead,
    ) -> None:
        if self.is_verified and current_user.is_verified != self.is_verified:
            raise ExceptionForbidden403(detail=ErrorCode.USER_NOT_VERIFIED)

        if self.is_active and current_user.is_active != self.is_active:
            raise ExceptionForbidden403(detail=ErrorCode.USER_INACTIVE)

        if self.is_superuser and current_user.is_superuser != self.is_superuser:
            raise ExceptionForbidden403(detail=ErrorCode.USER_NOT_ADMIN)

    async def validate_refresh_token(
        self,
        uow: IUnitOfWork,
        refresh_token: str,
    ) -> UserRead:
        payload: Mapping = JWTManager.decode_token(token=refresh_token)

        user_id: str | None = JWTManager.extract_from_payload(
            payload=payload, key="sub"
        )
        current_user: UserRead | None = await self._get_user_by_id(
            id=uuid.UUID(hex=user_id), uow=uow
        )

        if current_user is None:
            raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)

        return current_user

    async def _validate_refresh_token(
        self,
        uow: IUnitOfWork,
        refresh_token: str,
        device_id: str,
    ) -> UserRead:
        current_user: UserRead = await self.validate_refresh_token(
            refresh_token=refresh_token,
            uow=uow,
        )
        try:
            session_with_old_token: ActiveSessionInDB | None = (
                await self._get_session_by_user_and_token(
                    refresh_token=refresh_token,
                    user_id=current_user.id,
                    uow=uow,
                )
            )
            if session_with_old_token is None:
                raise ExceptionNotAcceptable406(detail=ErrorCode.INVALID_REFRESH_TOKEN)

            hashed_device_id: str = self._hash_text(text_for_hashing=device_id)

            if session_with_old_token.device_id != hashed_device_id:
                await self._delete_session_by_session_id(
                    session_id=session_with_old_token.id,
                    uow=uow,
                )
                raise ExceptionNotAcceptable406(detail=ErrorCode.INVALID_DEVICE_ID)

        except Exception as exception:
            raise exception

        await self.check_user_state(current_user=current_user)

        return current_user

    async def create_tokens(
        self,
        uow: IUnitOfWork,
        refresh_token: str,
        device_id: str,
    ) -> AccessRefreshTokens:
        authenticatd_user: UserRead = await self._validate_refresh_token(
            refresh_token=refresh_token,
            device_id=device_id,
            uow=uow,
        )

        return await self.generate_access_refresh_tokens(user=authenticatd_user)

    async def create_refresh_token(
        self,
        uow: IUnitOfWork,
        refresh_token: str,
        device_id: str,
    ) -> bytes:
        authenticatd_user: UserRead = await self._validate_refresh_token(
            refresh_token=refresh_token,
            device_id=device_id,
            uow=uow,
        )

        return await self._create_jwt_refresh_token(user_id=authenticatd_user.id)

    async def revoke_token(
        self,
        uow: IUnitOfWork,
        refresh_token: str,
    ) -> None:
        current_user: UserRead = await self.validate_refresh_token(
            refresh_token=refresh_token, uow=uow
        )
        await self.check_user_state(current_user=current_user)

        try:
            session_with_old_token: ActiveSessionInDB | None = (
                await self._get_session_by_user_and_token(
                    refresh_token=refresh_token,
                    user_id=current_user.id,
                    uow=uow,
                )
            )
            if session_with_old_token is None:
                raise ExceptionNotAcceptable406(detail=ErrorCode.INVALID_REFRESH_TOKEN)

            await self._delete_session_by_session_id(
                session_id=session_with_old_token.id,
                uow=uow,
            )

        except Exception as exception:
            raise exception

        return None
