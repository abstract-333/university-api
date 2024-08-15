from abc import ABC, abstractmethod
from models.lecturer_request import LecturersRequestsOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas.lecturer_request import LecturerRequestInDB
from schemas.pagination import Pagination
from specification.base import Specification
from sqlalchemy.ext.asyncio import AsyncSession


class LecturerRequestRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def add_lecturer_request(
        self,
        lecturer_request_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def edit_lecturer_request(
        self,
        lecturer_request_data: dict,
        specification: Specification,
    ) -> None:
        ...

    @abstractmethod
    async def get_lecturer_requests(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[LecturerRequestInDB] | None:
        ...

    @abstractmethod
    async def get_lecturer_request(
        self,
        specification: Specification,
    ) -> LecturerRequestInDB | None:
        ...


class LecturerRequestRepository(SQLAlchemyRepository, LecturerRequestRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[LecturersRequestsOrm] = LecturersRequestsOrm
        super().__init__(session=session)

    async def add_lecturer_request(
        self,
        lecturer_request_data: dict,
    ) -> None:
        await self.add_one(data=lecturer_request_data)

    async def edit_lecturer_request(
        self,
        lecturer_request_data: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(
            data=lecturer_request_data,
            arguments=specification.is_satisfied_by(),
        )

    async def get_lecturer_request(
        self, specification: Specification
    ) -> LecturerRequestInDB | None:
        lecturer_request_record: LecturerRequestInDB | None = await self.find_one(
            schema=LecturerRequestInDB,
            arguments=specification.is_satisfied_by(),
        )
        return lecturer_request_record

    async def get_lecturer_requests(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[LecturerRequestInDB] | None:
        lecturer_requests_records: list[
            LecturerRequestInDB
        ] | None = await self.find_by(
            schema=LecturerRequestInDB,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return lecturer_requests_records
