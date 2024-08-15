import time
import uuid

from common.unit_of_work import IUnitOfWork
from exception.base import ExceptionNotAcceptable406, ExceptionNotFound404
from exception.error_code import ErrorCode
from schemas.lecturer import LecturerInDB, LecturerCreate
from schemas.lecturer_request import (
    LecturerRequestInDB,
    LecturerRequestUpdate,
    LecturerRequestCreate,
    LecturerRequestProcessUpdate,
    LecturerRequestProcess,
)
from schemas.pagination import Pagination
from specification.lecturer import (
    LecturerFacultySpecification,
    LecturerIsApprovedSpecification,
    LecturerUserIdSpecification,
)
from specification.lecturer_request import (
    LecturerRequestFacultySpecification,
    LecturerRequestIdSpecification,
    LecturerRequestIsProcessedSpecification,
    LecturerRequestUserIdSpecification,
)


class LecturerRequestService:
    @classmethod
    async def _get_all_unprocessed_lecturer_requests(
        cls, user_id: uuid.UUID, uow: IUnitOfWork, pagination: Pagination
    ) -> list[LecturerRequestInDB] | None:
        async with uow:
            lecturer_requests: list[
                LecturerRequestInDB
            ] | None = await uow.lecturer_request.get_lecturer_requests(
                specification=~LecturerRequestIsProcessedSpecification()
                & LecturerRequestUserIdSpecification(user_id=user_id),
                pagination=pagination,
            )
            return lecturer_requests

    @classmethod
    async def _get_unprocessed_lecturer_request_by_faculty(
        cls,
        user_id: uuid.UUID,
        faculty_name: str,
        uow: IUnitOfWork,
    ) -> LecturerRequestInDB | None:
        async with uow:
            specification = (
                LecturerRequestFacultySpecification(faculty_name=faculty_name)
                & LecturerRequestUserIdSpecification(user_id=user_id)
                & ~LecturerRequestIsProcessedSpecification()
            )
            lecturer_request: LecturerRequestInDB | None = (
                await uow.lecturer_request.get_lecturer_request(
                    specification=specification
                )
            )
            return lecturer_request

    @classmethod
    async def _get_unprocessed_lecturer_request_by_id_user_id(
        cls,
        user_id: uuid.UUID,
        request_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> LecturerRequestInDB | None:
        async with uow:
            lecturer_request: LecturerRequestInDB | None = (
                await uow.lecturer_request.get_lecturer_request(
                    specification=LecturerRequestUserIdSpecification(user_id=user_id)
                    & LecturerRequestIdSpecification(id=request_id)
                    & ~LecturerRequestIsProcessedSpecification(),
                )
            )
            return lecturer_request

    @classmethod
    async def _get_unprocessed_lecturer_request_by_id(
        cls,
        request_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> LecturerRequestInDB | None:
        async with uow:
            lecturer_request: LecturerRequestInDB | None = (
                await uow.lecturer_request.get_lecturer_request(
                    specification=LecturerRequestIdSpecification(id=request_id)
                    & ~LecturerRequestIsProcessedSpecification(),
                )
            )
            return lecturer_request

    @classmethod
    async def _get_lecturer_by_faculty_user_id(
        cls,
        user_id: uuid.UUID,
        faculty_name: str,
        uow: IUnitOfWork,
    ) -> LecturerInDB | None:
        async with uow:
            lecturer: LecturerInDB | None = await uow.lecturer.get_lecturer(
                specification=LecturerUserIdSpecification(user_id=user_id)
                & LecturerFacultySpecification(faculty_name=faculty_name)
            )
            return lecturer

    @classmethod
    async def _add_lecturer_request(
        cls,
        lecturer_request_data: dict,
        lecturer_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.lecturer_request.add_lecturer_request(
                lecturer_request_data=lecturer_request_data
            )
            await uow.lecturer.add_lecturer(lecturer_data=lecturer_data)

            await uow.commit()

    @classmethod
    async def _edit_lecturer_request_by_user_id(
        cls,
        lecturer_request_data: dict,
        user_id: uuid.UUID,
        request_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.lecturer_request.edit_lecturer_request(
                lecturer_request_data=lecturer_request_data,
                specification=LecturerRequestUserIdSpecification(user_id=user_id)
                & LecturerRequestIdSpecification(id=request_id)
                & ~LecturerRequestIsProcessedSpecification(),
            )
            await uow.commit()

    @classmethod
    async def _edit_lecturer_request(
        cls,
        lecturer_request_data: dict,
        request_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.lecturer_request.edit_lecturer_request(
                lecturer_request_data=lecturer_request_data,
                specification=LecturerRequestIdSpecification(id=request_id)
                & ~LecturerRequestIsProcessedSpecification(),
            )
            await uow.commit()

    @classmethod
    async def _register_lecturer_accept_request(
        cls,
        lecturer_request_data: dict,
        lecturer_data: dict,
        request_id: uuid.UUID,
        user_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.lecturer_request.edit_lecturer_request(
                lecturer_request_data=lecturer_request_data,
                specification=LecturerRequestIdSpecification(id=request_id)
                & LecturerRequestUserIdSpecification(user_id=user_id)
                & ~LecturerRequestIsProcessedSpecification(),
            )
            await uow.lecturer.add_lecturer(lecturer_data=lecturer_data)

            await uow.commit()

    async def get_all_lecturer_requests(
        self,
        user_id: uuid.UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[LecturerRequestInDB] | None:
        try:
            lecturer_requests: list[
                LecturerRequestInDB
            ] | None = await self._get_all_unprocessed_lecturer_requests(
                user_id=user_id,
                pagination=pagination,
                uow=uow,
            )
            return lecturer_requests

        except Exception as e:
            raise e

    async def add_lecturer_request(
        self,
        lecturer_request_create: LecturerRequestCreate,
        uow: IUnitOfWork,
    ) -> None:
        try:
            if await self._is_lecturer_exist(
                user_id=lecturer_request_create.user_id,
                faculty_name=lecturer_request_create.faculty_name,
                uow=uow,
            ):
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.LECTURER_ALREADY_REGISTERED
                )

            old_requests: LecturerRequestInDB | None = (
                await self._get_unprocessed_lecturer_request_by_faculty(
                    user_id=lecturer_request_create.user_id,
                    faculty_name=lecturer_request_create.faculty_name,
                    uow=uow,
                )
            )
            if old_requests is not None:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.LECTURER_REQUEST_ALREADY_SENT
                )
            lecturer_data: dict[str, str] = LecturerCreate(
                user_id=lecturer_request_create.user_id,
                faculty_name=lecturer_request_create.faculty_name,
            ).model_dump()

            await self._add_lecturer_request(
                lecturer_request_data=lecturer_request_create.model_dump(),
                lecturer_data=lecturer_data,
                uow=uow,
            )
            return None

        except Exception as e:
            raise e

    async def edit_lecturer_request(
        self,
        request_id: uuid.UUID,
        user_id: uuid.UUID,
        lecturer_request_update: LecturerRequestUpdate,
        uow: IUnitOfWork,
    ) -> None:
        try:
            old_request: LecturerRequestInDB | None = (
                await self._get_unprocessed_lecturer_request_by_id_user_id(
                    user_id=user_id,
                    request_id=request_id,
                    uow=uow,
                )
            )

            if old_request is None:
                raise ExceptionNotFound404(detail=ErrorCode.LECTURER_REQUEST_NOT_EXISTS)

            if old_request != lecturer_request_update:
                await self._edit_lecturer_request_by_user_id(
                    lecturer_request_data=lecturer_request_update.model_dump(),
                    request_id=request_id,
                    user_id=user_id,
                    uow=uow,
                )

            return None

        except Exception as e:
            raise e

    async def accept_lecturer_request(
        self,
        lecturer_request: LecturerRequestProcess,
        uow: IUnitOfWork,
    ) -> None:
        try:
            if await self._is_lecturer_exist(
                user_id=lecturer_request.user_id,
                faculty_name=lecturer_request.faculty_name,
                uow=uow,
            ):
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.LECTURER_ALREADY_REGISTERED
                )

            if not await self._is_pending_request(
                request_id=lecturer_request.id, uow=uow
            ):
                raise ExceptionNotFound404(detail=ErrorCode.LECTURER_REQUEST_NOT_EXISTS)

            lecturer_data: dict[str, str] = LecturerCreate(
                user_id=lecturer_request.user_id,
                faculty_name=lecturer_request.faculty_name,
            ).model_dump()

            lecturer_request_data: dict[str, str] = LecturerRequestProcessUpdate(
                processed_at=int(time.time()), is_accepted=True
            ).model_dump()

            await self._register_lecturer_accept_request(
                lecturer_request_data=lecturer_request_data,
                lecturer_data=lecturer_data,
                request_id=lecturer_request.id,
                user_id=lecturer_request.user_id,
                uow=uow,
            )
            return None

        except Exception as exception:
            raise exception

    async def reject_lecturer_request(
        self,
        lecturer_request: LecturerRequestProcess,
        uow: IUnitOfWork,
    ) -> None:
        try:
            if not await self._is_pending_request(
                request_id=lecturer_request.id, uow=uow
            ):
                raise ExceptionNotFound404(detail=ErrorCode.LECTURER_REQUEST_NOT_EXISTS)

            lecturer_request_data: dict[str, str] = LecturerRequestProcessUpdate(
                processed_at=int(time.time()), is_accepted=False
            ).model_dump()

            await self._edit_lecturer_request(
                lecturer_request_data=lecturer_request_data,
                request_id=lecturer_request.id,
                uow=uow,
            )
            return None

        except Exception as exception:
            raise exception

    async def _is_pending_request(
        self,
        request_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> bool:
        try:
            old_lecturer_request: LecturerRequestInDB | None = (
                await self._get_unprocessed_lecturer_request_by_id(
                    request_id=request_id,
                    uow=uow,
                )
            )
            return old_lecturer_request is not None

        except Exception as exception:
            raise exception

    async def _is_lecturer_exist(
        self, user_id: uuid.UUID, faculty_name: str, uow: IUnitOfWork
    ) -> bool:
        try:
            lecturer_exists: LecturerInDB | None = (
                await self._get_lecturer_by_faculty_user_id(
                    user_id=user_id,
                    faculty_name=faculty_name,
                    uow=uow,
                )
            )
            return lecturer_exists is not None

        except Exception as exception:
            raise exception
