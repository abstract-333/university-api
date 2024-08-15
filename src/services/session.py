import base64
import hashlib
import uuid

from common.unit_of_work import IUnitOfWork
from exception.base import (
    ExceptionBadRequest400,
    ExceptionNotFound404,
)
from exception.error_code import ErrorCode
from schemas.active_session import ActiveSessionInDB, ActiveSessionOutput
from schemas.pagination import Pagination
from specification.active_session import (
    SessionDeviceIdSpecification,
    SessionIdSpecification,
    SessionUserIdSpecification,
)


class SessionService:
    @classmethod
    async def _get_all_sessions_user_id(
        cls,
        user_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[ActiveSessionInDB] | None:
        """Get all sessions by user_id"""
        async with uow:
            sessions: list[
                ActiveSessionInDB
            ] | None = await uow.active_session.get_sessions(
                specification=SessionUserIdSpecification(user_id=user_id),
                pagination=pagination,
            )

            return sessions

    @classmethod
    async def _get_sessions_by_user_device_or_id(
        cls,
        device_id: str,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> list[ActiveSessionInDB] | None:
        """Get all sessions by user_id and (device_id or session_id)"""
        async with uow:
            sessions: list[
                ActiveSessionInDB
            ] | None = await uow.active_session.get_sessions(
                specification=SessionUserIdSpecification(user_id=user_id)
                & (
                    SessionDeviceIdSpecification(device_id=device_id)
                    | SessionIdSpecification(session_id=session_id)
                )
            )
            return sessions

    @classmethod
    async def _get_session_by_device(
        cls,
        device_id: str,
        user_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> ActiveSessionInDB | None:
        """Get single session by device_id and user_id or return None"""
        async with uow:
            session: ActiveSessionInDB | None = await uow.active_session.get_session(
                specification=SessionUserIdSpecification(user_id=user_id)
                & SessionDeviceIdSpecification(device_id=device_id)
            )

            return session

    @classmethod
    async def _delete_session_by_session_id(
        cls, session_id: uuid.UUID, uow: IUnitOfWork
    ) -> None:
        """Delete session by session_id"""
        async with uow:
            await uow.active_session.delete_session(
                specification=SessionIdSpecification(session_id=session_id)
            )
            await uow.commit()

    async def get_all_sessions_for_user(
        self,
        user_id: uuid.UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[ActiveSessionOutput] | None:
        """Return all sessions that user have now"""

        try:
            sessions: list[
                ActiveSessionInDB
            ] | None = await self._get_all_sessions_user_id(
                user_id=user_id, pagination=pagination, uow=uow
            )
            if sessions is not None:
                validated_sessions: list[ActiveSessionOutput] | None = [
                    ActiveSessionOutput(**session.model_dump()) for session in sessions
                ]
                return validated_sessions

            return sessions

        except Exception as exception:
            raise exception

    @classmethod
    def _hash_text(cls, text_for_hashing: str) -> str:
        hashed_text = hashlib.sha256(string=text_for_hashing.encode())
        hashed_bytes: bytes = hashed_text.digest()
        hashed_string: str = base64.b64encode(hashed_bytes).decode()
        return hashed_string

    async def get_session(
        self,
        device_id: str,
        user_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> ActiveSessionOutput | None:
        """Return Single Session by device_id"""
        try:
            hashed_device_id: str = self._hash_text(text_for_hashing=device_id)

            session: ActiveSessionInDB | None = await self._get_session_by_device(
                device_id=hashed_device_id,
                user_id=user_id,
                uow=uow,
            )

            if session is not None:
                return ActiveSessionOutput(**session.model_dump())

            return session

        except Exception as exception:
            raise exception

    async def delete_newer_session(
        self,
        session_id: uuid.UUID,
        current_device_id: str,
        user_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        try:
            hashed_device_id: str = self._hash_text(text_for_hashing=current_device_id)

            user_sessions: list[
                ActiveSessionInDB
            ] | None = await self._get_sessions_by_user_device_or_id(
                user_id=user_id,
                device_id=hashed_device_id,
                session_id=session_id,
                uow=uow,
            )

            # Ensure that sessions exists
            if user_sessions is None or len(user_sessions) == 1:
                raise ExceptionNotFound404(detail=ErrorCode.SESSION_NOT_EXISTS)

            # Ensure that deleted session is newer the current session
            if user_sessions[0].id == session_id:
                raise ExceptionBadRequest400(detail=ErrorCode.SESSION_MUST_BE_OLDER)

            await self._delete_session_by_session_id(session_id=session_id, uow=uow)

        except Exception as exception:
            raise exception
