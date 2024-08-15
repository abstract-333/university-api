from abc import ABC, abstractmethod

from models.file import FilesOrm
from respository.base import AbstractSQLRepository, SQLAlchemyRepository
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.file import FileInDB
from schemas.pagination import Pagination
from specification.base import Specification


class FileRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def get_files(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[FileInDB] | None:
        ...

    @abstractmethod
    async def get_file(
        self,
        specification: Specification,
    ) -> FileInDB | None:
        ...

    @abstractmethod
    async def add_file(
        self,
        file_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def edit_file(
        self,
        file_data: dict,
        specification: Specification,
    ) -> None:
        ...

    @abstractmethod
    async def delete_file(
        self,
        specification: Specification,
    ) -> None:
        ...


class FileRepository(SQLAlchemyRepository, FileRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[FilesOrm] = FilesOrm
        super().__init__(session=session)

    async def add_file(
        self,
        file_data: dict,
    ) -> None:
        await self.add_one(
            data=file_data,
        )

    async def edit_file(
        self,
        file_data: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(
            data=file_data,
            arguments=specification.is_satisfied_by(),
        )

    async def get_file(self, specification: Specification) -> FileInDB | None:
        return await self.find_one(
            arguments=specification.is_satisfied_by(),
            schema=FileInDB,
        )

    async def get_files(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[FileInDB] | None:
        return await self.find_by(
            arguments=specification.is_satisfied_by(),
            schema=FileInDB,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    async def delete_file(
        self,
        specification: Specification,
    ) -> None:
        return await self.delete_one(
            arguments=specification.is_satisfied_by(),
        )
