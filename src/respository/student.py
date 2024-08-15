from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from models import StudentsOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas import StudentInDBWithSpeciality
from schemas.pagination import Pagination
from schemas.student import StudentInDB
from specification.base import Specification
from sqlalchemy.orm import joinedload, selectinload


class StudentRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def add_student(self, student_data: dict) -> None:
        ...

    @abstractmethod
    async def get_students(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[StudentInDB] | None:
        ...

    @abstractmethod
    async def get_student(
        self,
        specification: Specification,
    ) -> StudentInDB | None:
        ...

    @abstractmethod
    async def get_students_with_speciality(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[StudentInDBWithSpeciality] | None:
        ...

    @abstractmethod
    async def get_student_with_speciality(
        self,
        specification: Specification,
    ) -> StudentInDBWithSpeciality | None:
        ...

    @abstractmethod
    async def edit_student(
        self, student_edit: dict, specification: Specification
    ) -> None:
        ...


class StudentRepository(SQLAlchemyRepository, StudentRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: Type[StudentsOrm] = StudentsOrm
        super().__init__(session=session)

    async def add_student(
        self,
        student_data: dict,
    ) -> None:
        await self.add_one(data=student_data)

    async def get_students_with_speciality(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[StudentInDBWithSpeciality] | None:
        students: list[StudentInDBWithSpeciality] | None = await self.find_by(
            joinedload(self.model_cls.speciality),
            schema=StudentInDBWithSpeciality,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return students

    async def get_student_with_speciality(
        self,
        specification: Specification,
    ) -> StudentInDBWithSpeciality | None:
        student: StudentInDBWithSpeciality | None = await self.find_one(
            joinedload(self.model_cls.speciality),
            schema=StudentInDBWithSpeciality,
            arguments=specification.is_satisfied_by(),
        )
        return student

    async def get_student(self, specification: Specification) -> StudentInDB | None:
        student: StudentInDB | None = await self.find_one(
            schema=StudentInDB,
            arguments=specification.is_satisfied_by(),
        )
        return student

    async def get_students(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[StudentInDB] | None:
        students: list[StudentInDB] | None = await self.find_by(
            schema=StudentInDB,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return students

    async def edit_student(
        self,
        student_edit: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(
            data=student_edit,
            arguments=specification.is_satisfied_by(),
        )
