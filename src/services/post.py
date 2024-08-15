import uuid

from common.unit_of_work import IUnitOfWork
from exception.base import ExceptionMethodNotAllowed405, ExceptionNotFound404
from exception.error_code import ErrorCode
from schemas.course_lecturer import CourseLecturerInDB
from schemas.enrolled_course import EnrolledCourseInDB
from schemas.pagination import Pagination
from schemas.post import (
    PostCreate,
    PostInDB,
    PostInDBExtended,
    PostUpdate,
    PostInDBExtendedWithoutComments,
)
from specification.course_lecturer import (
    CourseLecturerCourseIDSpecification,
    CourseLecturerIdSpecification,
    CourseLecturerLecturerIdSpecification,
)
from specification.enrolled_course import (
    EnrolledCourseIdSpecification,
    EnrolledCourseStudentIdSpecification,
)
from specification.post import PostCourseIdSpecification, PostIdSpecification


class PostService:
    @classmethod
    async def _get_post_detailed_with_comments(
        cls,
        post_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> PostInDBExtended | None:
        async with uow:
            return await uow.post.get_post_detailed_with_comments(
                specification=PostIdSpecification(id=post_id)
            )

    @classmethod
    async def _get_posts_detailed_without_comments(
        cls,
        course_id: uuid.UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[PostInDBExtendedWithoutComments] | None:
        async with uow:
            return await uow.post.get_posts_detailed_without_comments(
                specification=CourseLecturerCourseIDSpecification(course_id=course_id),
                pagination=pagination,
            )

    @classmethod
    async def _get_posts_for_me(
        cls,
        course_lecturer_id: uuid.UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[PostInDB] | None:
        async with uow:
            return await uow.post.get_posts(
                specification=PostCourseIdSpecification(course_id=course_lecturer_id),
                pagination=pagination,
            )

    @classmethod
    async def _get_posts_by_taught_course_id(
        cls,
        taught_course_id: uuid.UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[PostInDBExtendedWithoutComments] | None:
        async with uow:
            return await uow.post.get_posts_detailed_without_comments(
                specification=CourseLecturerCourseIDSpecification(
                    course_id=taught_course_id
                ),
                pagination=pagination,
            )

    @classmethod
    async def _get_post(
        cls,
        post_id: uuid.UUID,
        course_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> PostInDB | None:
        async with uow:
            return await uow.post.get_post(
                specification=PostIdSpecification(id=post_id)
                & PostCourseIdSpecification(course_id=course_id)
            )

    @classmethod
    async def _get_enrolled_course(
        cls,
        enrolled_course_id: uuid.UUID,
        student_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> EnrolledCourseInDB | None:
        async with uow:
            enrolled_course: EnrolledCourseInDB | None = (
                await uow.enrolled_course.get_enrolled_course(
                    specification=EnrolledCourseIdSpecification(id=enrolled_course_id)
                    & EnrolledCourseStudentIdSpecification(student_id=student_id)
                )
            )
            return enrolled_course

    @classmethod
    async def _add_post(
        cls,
        post_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.post.add_post(post_data=post_data)
            await uow.commit()

    @classmethod
    async def _get_course_lecturer(
        cls,
        course_lecturer_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> CourseLecturerInDB | None:
        async with uow:
            return await uow.course_lecturer.get_course_lecturer(
                specification=CourseLecturerLecturerIdSpecification(
                    lecturer_id=lecturer_id
                )
                & CourseLecturerIdSpecification(id=course_lecturer_id),
            )

    @classmethod
    async def _edit_post(
        cls,
        post_id: uuid.UUID,
        course_lecturer_id: uuid.UUID,
        post_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        """Edit post by course_lecturer_id

        Args:
            post_id (uuid.UUID):

            course_lecturer_id (uuid.UUID):

            post_data (dict):

            uow (IUnitOfWork):
        """
        async with uow:
            await uow.post.edit_post(
                post_data=post_data,
                specification=PostCourseIdSpecification(course_id=course_lecturer_id)
                & PostIdSpecification(id=post_id),
            )
            await uow.commit()

    @classmethod
    async def _delete_post(
        cls,
        post_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        """Delete post by post_id

        Args:
            post_id (uuid.UUID):

            uow (IUnitOfWork):
        """
        async with uow:
            await uow.post.delete_post(specification=PostIdSpecification(id=post_id))
            await uow.commit()

    async def add_post(
        self,
        post_create: PostCreate,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        """add post

        Args:
            post_create (PostCreate):

            lecturer_id (uuid.UUID):

            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE

            exception:

        Returns:
            _type_: None
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=post_create.lecturer_course_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )

            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            await self._add_post(
                post_data=post_create.model_dump(),
                uow=uow,
            )
            return None

        except Exception as exception:
            raise exception

    async def get_posts_course_student(
        self,
        enrolled_course_id: uuid.UUID,
        student_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[PostInDBExtendedWithoutComments] | None:
        try:
            enrolled_course: EnrolledCourseInDB | None = (
                await self._get_enrolled_course(
                    enrolled_course_id=enrolled_course_id,
                    student_id=student_id,
                    uow=uow,
                )
            )

            if enrolled_course is None:
                raise ExceptionMethodNotAllowed405(
                    detail=ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE
                )

            return await self._get_posts_by_taught_course_id(
                taught_course_id=enrolled_course.taught_course_id,
                uow=uow,
                pagination=pagination,
            )

        except Exception as exception:
            raise exception

    async def get_post_detailed_for_student(
        self,
        enrolled_course_id: uuid.UUID,
        student_id: uuid.UUID,
        post_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> PostInDBExtended | None:
        try:
            enrolled_course: EnrolledCourseInDB | None = (
                await self._get_enrolled_course(
                    enrolled_course_id=enrolled_course_id,
                    student_id=student_id,
                    uow=uow,
                )
            )

            if enrolled_course is None:
                raise ExceptionMethodNotAllowed405(
                    detail=ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE
                )

            return await self._get_post_detailed_with_comments(
                post_id=post_id,
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def get_post_detailed_for_lecturer(
        self,
        course_lecturer_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        post_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> PostInDBExtended | None:
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=course_lecturer_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )

            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            return await self._get_post_detailed_with_comments(
                post_id=post_id,
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def get_posts_added_lecturer(
        self,
        course_lecturer_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[PostInDB] | None:
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=course_lecturer_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )

            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            return await self._get_posts_for_me(
                course_lecturer_id=course_lecturer_id,
                uow=uow,
                pagination=pagination,
            )

        except Exception as exception:
            raise exception

    async def get_posts_for_course_lecturer(
        self,
        course_lecturer_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[PostInDBExtendedWithoutComments] | None:
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=course_lecturer_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )

            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            return await self._get_posts_by_taught_course_id(
                taught_course_id=course_lecturer.course_id,
                uow=uow,
                pagination=pagination,
            )

        except Exception as exception:
            raise exception

    async def update_post(
        self,
        post_update: PostUpdate,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        """edit post

        Args:
            post_update (PostUpdate):

            lecturer_id (uuid.UUID):

            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE

            ExceptionNotFound404: POST_NOT_FOUND

            exception: _description_

        Returns:
            _type_: None
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=post_update.lecturer_course_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )

            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            post: PostInDB | None = await self._get_post(
                post_id=post_update.id,
                course_id=post_update.lecturer_course_id,
                uow=uow,
            )

            if post is None:
                raise ExceptionNotFound404(detail=ErrorCode.POST_NOT_FOUND)

            await self._edit_post(
                post_id=post_update.id,
                course_lecturer_id=post_update.lecturer_course_id,
                post_data=post_update.model_dump(),
                uow=uow,
            )
            return None

        except Exception as exception:
            raise exception

    async def delete_post(
        self,
        post_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        course_lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        """delete post

        Args:
            post_id (uuid.UUID): _description_
            lecturer_id (uuid.UUID): _description_
            course_lecturer_id (uuid.UUID): _description_
            uow (IUnitOfWork): _description_

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE

            ExceptionNotFound404: POST_NOT_FOUND

            exception: _description_

        Returns:
            _type_: _description_
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=course_lecturer_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )

            if course_lecturer is None:
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            post: PostInDB | None = await self._get_post(
                post_id=post_id,
                course_id=course_lecturer_id,
                uow=uow,
            )

            if post is None:
                raise ExceptionNotFound404(detail=ErrorCode.POST_NOT_FOUND)

            await self._delete_post(
                post_id=post_id,
                uow=uow,
            )

            return None

        except Exception as exception:
            raise exception
