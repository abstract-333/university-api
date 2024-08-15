from typing import Mapping
import uuid

from fastapi import Depends
from fastapi.security import HTTPBearer
from common import IUnitOfWork
from common.jwt import JWTManager
from exception import ExceptionNotAcceptable406
from exception.base import ExceptionNotFound404
from exception.error_code import ErrorCode
from schemas import LecturerInDB
from schemas.lecturer import LecturerCreate
from schemas.pagination import Pagination
from specification.lecturer import (
    LecturerIdSpecification,
    LecturerIsApprovedSpecification,
    LecturerUserIdSpecification,
)
from settings.settings import settings_obj

oauth2_lecturer_scheme = HTTPBearer(scheme_name="Lecturer")


class LecturerService:
    @classmethod
    async def _get_lecturers(
        cls,
        uow: IUnitOfWork,
        user_id: uuid.UUID,
        pagination: Pagination,
    ) -> list[LecturerInDB] | None:
        async with uow:
            lecturer_list: list[LecturerInDB] | None = await uow.lecturer.get_lecturers(
                specification=LecturerUserIdSpecification(user_id=user_id),
                pagination=pagination,
            )
            return lecturer_list

    @classmethod
    async def _get_lecturer_by_id(
        cls,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> LecturerInDB | None:
        """Get lecturer from by lecturer_id"""
        async with uow:
            lecturer: LecturerInDB | None = await uow.lecturer.get_lecturer(
                specification=LecturerIdSpecification(lecturer_id=lecturer_id)
                & LecturerIsApprovedSpecification()
            )
            return lecturer

    @classmethod
    async def _add_lecturer(cls, lecturer_data: dict, uow: IUnitOfWork) -> None:
        async with uow:
            await uow.lecturer.add_lecturer(lecturer_data=lecturer_data)
            await uow.commit()

    async def get_current_lecturer(
        self,
        token: str = Depends(dependency=oauth2_lecturer_scheme),
    ) -> LecturerInDB:
        current_lecturer: LecturerInDB = await self._extract_lecturer_from_token(
            token=token.credentials
        )
        return current_lecturer

    @classmethod
    async def _extract_lecturer_from_token(cls, token: str) -> LecturerInDB:
        payload: Mapping = JWTManager.decode_token(token=token)
        lecturer: Mapping | None = JWTManager.extract_from_payload(
            payload=payload, key="lecturer"
        )
        if lecturer is None:
            raise ExceptionNotFound404(detail=ErrorCode.LECTURER_NOT_EXISTS)

        lecturer_model = LecturerInDB(**lecturer)
        return lecturer_model

    async def make_token_lecturer(
        self, lecturer_id: uuid.UUID, uow: IUnitOfWork
    ) -> bytes:
        lecturer: LecturerInDB | None = await self._get_lecturer_by_id(
            lecturer_id=lecturer_id, uow=uow
        )
        if lecturer is None:
            raise ExceptionNotFound404(detail=ErrorCode.LECTURER_NOT_EXISTS)

        token: bytes = await self._create_jwt_access_token(lecturer=lecturer)

        return token

    @classmethod
    async def _create_jwt_access_token(cls, lecturer: LecturerInDB) -> bytes:
        jwt_token: bytes = JWTManager.create_jwt_token(
            valid_duration=settings_obj.JWT_EXPIRATION_ACCESS_TOKEN,
            lecturer=lecturer.model_dump(mode="json"),
        )
        return jwt_token

    async def register_lecturer(
        self,
        uow: IUnitOfWork,
        lecturer_data: LecturerCreate,
    ) -> None:
        try:
            await self._add_lecturer(lecturer_data=lecturer_data.model_dump(), uow=uow)

        except Exception:
            raise ExceptionNotAcceptable406(detail=ErrorCode.INVALID_CREDENTIALS)

        return None

    async def get_lecturer_records_by_user_id(
        self, user_id: uuid.UUID, uow: IUnitOfWork, pagination: Pagination
    ) -> list[LecturerInDB] | None:
        return await self._get_lecturers(
            user_id=user_id, pagination=pagination, uow=uow
        )
