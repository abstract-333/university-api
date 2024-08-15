from abc import ABC, abstractmethod

from models.comment import CommentsOrm
from models.lecturer import LecturersOrm
from models.student import StudentsOrm
from respository.base import AbstractSQLRepository, SQLAlchemyRepository
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.comment import CommentInDB, CommentInDBExtended
from schemas.pagination import Pagination
from specification.base import Specification


class CommentRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def get_comments_for_post(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CommentInDBExtended] | None:
        ...

    @abstractmethod
    async def get_comment(
        self,
        specification: Specification,
    ) -> CommentInDB | None:
        ...

    @abstractmethod
    async def add_comment(
        self,
        comment_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def edit_comment(
        self,
        comment_data: dict,
        specification: Specification,
    ) -> None:
        ...

    @abstractmethod
    async def delete_comment(
        self,
        specification: Specification,
    ) -> None:
        ...


class CommentRepository(SQLAlchemyRepository, CommentRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[CommentsOrm] = CommentsOrm
        super().__init__(session=session)

    async def add_comment(
        self,
        comment_data: dict,
    ) -> None:
        await self.add_one(
            data=comment_data,
        )

    async def edit_comment(
        self,
        comment_data: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(
            data=comment_data,
            arguments=specification.is_satisfied_by(),
        )

    async def get_comment(self, specification: Specification) -> CommentInDB | None:
        return await self.find_one(
            arguments=specification.is_satisfied_by(),
            schema=CommentInDB,
        )

    async def get_comments_for_post(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[CommentInDBExtended] | None:
        return await self.find_by(
            joinedload(self.model_cls.student).joinedload(StudentsOrm.user),
            joinedload(self.model_cls.student).joinedload(StudentsOrm.speciality),
            joinedload(self.model_cls.lecturer).joinedload(LecturersOrm.user),
            arguments=specification.is_satisfied_by(),
            schema=CommentInDBExtended,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    async def delete_comment(
        self,
        specification: Specification,
    ) -> None:
        return await self.delete_one(
            arguments=specification.is_satisfied_by(),
        )
