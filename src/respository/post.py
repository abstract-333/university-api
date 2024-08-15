from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from models.comment import CommentsOrm
from models.course_lecturer import CoursesLecturersOrm
from models.lecturer import LecturersOrm
from models.post import PostsOrm
from models.speciality_course import SpecialityCoursesOrm
from models.student import StudentsOrm
from models.taught_courses import TaughtCoursesOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas.pagination import Pagination
from schemas.post import PostInDB, PostInDBExtended, PostInDBExtendedWithoutComments
from specification.base import Specification


class PostRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def add_post(
        self,
        post_data: dict,
    ) -> None:
        ...

    @abstractmethod
    async def edit_post(
        self,
        post_data: dict,
        specification: Specification,
    ) -> None:
        ...

    @abstractmethod
    async def get_posts(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[PostInDB] | None:
        ...

    @abstractmethod
    async def get_post_detailed_with_comments(
        self,
        specification: Specification,
    ) -> PostInDBExtended | None:
        ...

    @abstractmethod
    async def get_posts_detailed_without_comments(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[PostInDBExtendedWithoutComments] | None:
        ...

    @abstractmethod
    async def get_post(
        self,
        specification: Specification,
    ) -> PostInDB | None:
        ...

    @abstractmethod
    async def delete_post(
        self,
        specification: Specification,
    ) -> None:
        ...


class PostRepository(SQLAlchemyRepository, PostRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[PostsOrm] = PostsOrm
        super().__init__(session=session)

    async def add_post(
        self,
        post_data: dict,
    ) -> None:
        await self.add_one(data=post_data)

    async def get_posts(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[PostInDB] | None:
        posts: list[PostInDB] | None = await self.find_by(
            schema=PostInDB,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return posts

    async def get_post_detailed_with_comments(
        self,
        specification: Specification,
    ) -> PostInDBExtended | None:
        post: PostInDBExtended | None = await self.find_one(
            joinedload(self.model_cls.lecturer_course)
            .joinedload(CoursesLecturersOrm.lecturer)
            .joinedload(LecturersOrm.user),
            joinedload(self.model_cls.lecturer_course)
            .joinedload(CoursesLecturersOrm.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            selectinload(self.model_cls.comments)
            .joinedload(CommentsOrm.student)
            .joinedload(StudentsOrm.user),
            selectinload(self.model_cls.comments)
            .joinedload(CommentsOrm.lecturer)
            .joinedload(LecturersOrm.user),
            join_conditions=(self.model_cls.lecturer_course,),
            schema=PostInDBExtended,
            arguments=specification.is_satisfied_by(),
        )
        return post

    async def get_posts_detailed_without_comments(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[PostInDBExtendedWithoutComments] | None:
        posts: list[PostInDBExtendedWithoutComments] | None = await self.find_by(
            joinedload(self.model_cls.lecturer_course)
            .joinedload(CoursesLecturersOrm.lecturer)
            .joinedload(LecturersOrm.user),
            joinedload(self.model_cls.lecturer_course)
            .joinedload(CoursesLecturersOrm.course)
            .joinedload(TaughtCoursesOrm.speciality_course)
            .joinedload(SpecialityCoursesOrm.speciality),
            join_conditions=(self.model_cls.lecturer_course,),
            schema=PostInDBExtendedWithoutComments,
            arguments=specification.is_satisfied_by(),
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return posts

    async def get_post(
        self,
        specification: Specification,
    ) -> PostInDB | None:
        return await self.find_one(
            schema=PostInDB,
            arguments=specification.is_satisfied_by(),
        )

    async def edit_post(
        self,
        post_data: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(arguments=specification.is_satisfied_by(), data=post_data)

    async def delete_post(
        self,
        specification: Specification,
    ) -> None:
        await self.delete_one(
            arguments=specification.is_satisfied_by(),
        )
