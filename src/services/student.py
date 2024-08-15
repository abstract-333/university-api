from typing import Mapping
import uuid
from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
)
from common import IUnitOfWork
from common.jwt import JWTManager
from exception import ExceptionNotAcceptable406
from exception.base import ExceptionNotFound404
from exception.error_code import ErrorCode
from schemas import StudentInDBWithSpeciality, StudentUpdate
from schemas.pagination import Pagination
from schemas.student import StudentCreateFull, StudentInDB, StudentUpdateState
from specification.student import (
    StudentIdSpecification,
    StudentSpecialityIdSpecification,
    StudentUniversityIdSpecification,
    StudentUserIdSpecification,
)
from settings.settings import settings_obj

oauth2_student_scheme = HTTPBearer(scheme_name="Student")


class StudentService:
    @classmethod
    async def get_students_with_speciality(
        cls,
        uow: IUnitOfWork,
        user_id: uuid.UUID,
        pagination: Pagination,
    ) -> list[StudentInDBWithSpeciality] | None:
        """Return students with speciality value"""
        async with uow:
            students: list[
                StudentInDBWithSpeciality
            ] | None = await uow.student.get_students_with_speciality(
                specification=StudentUserIdSpecification(user_id=user_id),
                pagination=pagination,
            )
            return students

    @classmethod
    async def get_student_by_id_with_speciality(
        cls,
        uow: IUnitOfWork,
        student_id: uuid.UUID,
    ) -> StudentInDBWithSpeciality | None:
        """Return student with speciality value"""

        async with uow:
            student: StudentInDBWithSpeciality | None = (
                await uow.student.get_student_with_speciality(
                    specification=StudentIdSpecification(id=student_id),
                )
            )
            return student

    @classmethod
    async def _get_student(
        cls,
        speciality_id: uuid.UUID,
        user_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> StudentInDB | None:
        async with uow:
            return await uow.student.get_student(
                specification=StudentUserIdSpecification(user_id=user_id)
                & StudentSpecialityIdSpecification(speciality_id=speciality_id),
            )

    @classmethod
    async def add_student(cls, uow: IUnitOfWork, create_student: dict) -> None:
        async with uow:
            await uow.student.add_student(student_data=create_student)
            await uow.commit()

    @classmethod
    async def edit_student_by_user_id(
        cls,
        uow: IUnitOfWork,
        student_edit: dict,
        student_id: uuid.UUID,
    ) -> None:
        async with uow:
            student_filter_id_user_id_specification = StudentIdSpecification(
                id=student_id
            )
            await uow.student.edit_student(
                student_edit=student_edit,
                specification=student_filter_id_user_id_specification,
            )
            await uow.commit()

    async def get_current_student(
        self,
        token: str = Depends(dependency=oauth2_student_scheme),
    ) -> StudentInDBWithSpeciality:
        current_student: StudentInDBWithSpeciality = (
            await self.extract_student_from_token(token=token.credentials)
        )
        return current_student

    async def make_token_student(
        self, student_id: uuid.UUID, uow: IUnitOfWork
    ) -> bytes:
        student: StudentInDBWithSpeciality | None = (
            await self.get_student_by_id_with_speciality(student_id=student_id, uow=uow)
        )
        print(student)
        if student is None:
            raise ExceptionNotFound404(detail=ErrorCode.STUDENT_NOT_EXISTS)

        token: bytes = await self.create_jwt_access_token(student=student)

        return token

    @classmethod
    async def create_jwt_access_token(cls, student: StudentInDBWithSpeciality) -> bytes:
        jwt_token: bytes = JWTManager.create_jwt_token(
            valid_duration=settings_obj.JWT_EXPIRATION_ACCESS_TOKEN,
            student=student.model_dump(mode="json"),
        )
        return jwt_token

    async def extract_student_from_token(self, token: str) -> StudentInDBWithSpeciality:
        payload: Mapping = JWTManager.decode_token(token=token)
        student: Mapping | None = JWTManager.extract_from_payload(
            payload=payload, key="student"
        )

        if student is None:
            raise ExceptionNotFound404(detail=ErrorCode.STUDENT_NOT_EXISTS)

        student_model = StudentInDBWithSpeciality(**student)
        return student_model

    async def register_student(
        self,
        uow: IUnitOfWork,
        create_student: StudentCreateFull,
    ) -> None:
        try:
            student: StudentInDB | None = await self._get_student(
                speciality_id=create_student.speciality_id,
                user_id=create_student.user_id,
                uow=uow,
            )
            if student is not None:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.INVALID_CREDENTIALS,
                )

            await self.add_student(create_student=create_student.model_dump(), uow=uow)

        except Exception as exception:
            raise exception

        return None

    async def update_student(
        self,
        uow: IUnitOfWork,
        updated_student: StudentUpdate,
        student_id: uuid.UUID,
    ) -> StudentUpdate:
        try:
            await self.edit_student_by_user_id(
                student_edit=updated_student.model_dump(
                    exclude_unset=True,
                    exclude_none=True,
                    exclude_defaults=True,
                ),
                uow=uow,
                student_id=student_id,
            )
            return updated_student

        except Exception:
            raise ExceptionNotAcceptable406(detail=ErrorCode.INVALID_CREDENTIALS)

    async def update_student_state(
        self,
        uow: IUnitOfWork,
        updated_student: StudentUpdateState,
        student_id: uuid.UUID,
    ) -> StudentUpdateState:
        try:
            await self.edit_student_by_user_id(
                student_edit=updated_student.model_dump(
                    exclude_unset=True,
                    exclude_none=True,
                    exclude_defaults=True,
                ),
                uow=uow,
                student_id=student_id,
            )
            return updated_student
        except Exception:
            raise ExceptionNotAcceptable406(detail=ErrorCode.INVALID_CREDENTIALS)

    async def get_students_by_user_id(
        self,
        uow: IUnitOfWork,
        user_id: uuid.UUID,
        pagination: Pagination = Pagination(),
    ) -> list[StudentInDBWithSpeciality] | None:
        return await self.get_students_with_speciality(
            pagination=pagination, user_id=user_id, uow=uow
        )
