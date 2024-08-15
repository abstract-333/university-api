from uuid import UUID

from common.unit_of_work import IUnitOfWork
from exception.base import ExceptionNotAcceptable406, ExceptionNotFound404
from exception.error_code import ErrorCode
from schemas.comment import AuthorType, CommentCreate, CommentInDB, CommentInDBExtended
from schemas.course_lecturer import CourseLecturerInDB
from schemas.enrolled_course import EnrolledCourseInDB
from schemas.pagination import Pagination
from schemas.post import PostInDB
from specification.comment import (
    CommentIdSpecification,
    CommentLecturerIdSpecification,
    CommentPostIdSpecification,
    CommentStudentIdSpecification,
)
from specification.course_lecturer import (
    CourseLecturerIdSpecification,
    CourseLecturerLecturerIdSpecification,
)
from specification.enrolled_course import (
    EnrolledCourseIdSpecification,
    EnrolledCourseStudentIdSpecification,
)
from specification.post import PostIdSpecification


class CommentService:
    @classmethod
    async def _add_comment(
        cls,
        comment_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.comment.add_comment(comment_data=comment_data)
            await uow.commit()

    @classmethod
    async def _update_comment(
        cls,
        comment_data: dict,
        comment_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.comment.edit_comment(
                comment_data=comment_data,
                specification=CommentIdSpecification(id=comment_id),
            )
            await uow.commit()

    @classmethod
    async def _delete_comment(
        cls,
        comment_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.comment.delete_comment(
                specification=CommentIdSpecification(id=comment_id),
            )
            await uow.commit()

    @classmethod
    async def _get_post(
        cls,
        post_id: UUID,
        uow: IUnitOfWork,
    ) -> PostInDB | None:
        async with uow:
            return await uow.post.get_post(
                specification=PostIdSpecification(id=post_id)
            )

    @classmethod
    async def _get_comments_for_post(
        cls,
        post_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[CommentInDBExtended] | None:
        async with uow:
            return await uow.comment.get_comments_for_post(
                specification=CommentPostIdSpecification(
                    post_id=post_id,
                ),
                pagination=pagination,
            )

    @classmethod
    async def _get_comments_for_post_by_student(
        cls,
        post_id: UUID,
        student_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[CommentInDBExtended] | None:
        async with uow:
            return await uow.comment.get_comments_for_post(
                specification=CommentPostIdSpecification(
                    post_id=post_id,
                )
                & CommentStudentIdSpecification(student_id=student_id),
                pagination=pagination,
            )

    @classmethod
    async def _get_comments_for_post_by_lecturer(
        cls,
        post_id: UUID,
        lecturer_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[CommentInDBExtended] | None:
        async with uow:
            return await uow.comment.get_comments_for_post(
                specification=CommentPostIdSpecification(
                    post_id=post_id,
                )
                & CommentLecturerIdSpecification(lecturer_id=lecturer_id),
                pagination=pagination,
            )

    @classmethod
    async def _get_comment_for_lecturer(
        cls,
        comment_id: UUID,
        lecturer_id: UUID,
        uow: IUnitOfWork,
    ) -> CommentInDB | None:
        async with uow:
            return await uow.comment.get_comment(
                specification=CommentIdSpecification(id=comment_id)
                & CommentLecturerIdSpecification(lecturer_id=lecturer_id)
            )

    @classmethod
    async def _get_comment_for_student(
        cls,
        comment_id: UUID,
        student_id: UUID,
        uow: IUnitOfWork,
    ) -> CommentInDB | None:
        async with uow:
            return await uow.comment.get_comment(
                specification=CommentIdSpecification(id=comment_id)
                & CommentStudentIdSpecification(student_id=student_id)
            )

    @classmethod
    async def _get_course_lecturer(
        cls,
        course_lecturer_id: UUID,
        lecturer_id: UUID,
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
    async def _get_enrolled_course(
        cls,
        enrolled_course_id: UUID,
        student_id: UUID,
        uow: IUnitOfWork,
    ) -> EnrolledCourseInDB | None:
        async with uow:
            return await uow.enrolled_course.get_enrolled_course(
                specification=EnrolledCourseStudentIdSpecification(
                    student_id=student_id
                )
                & EnrolledCourseIdSpecification(id=enrolled_course_id)
            )

    async def get_comments_for_post_by_lecturer(
        self,
        post_id: UUID,
        course_lecturer_id: UUID,
        lecturer_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[CommentInDBExtended] | None:
        """Get comments for post (Lecturer can use this method)

        Args:
            post_id (UUID): _description_
            course_lecturer_id (UUID): _description_
            lecturer_id (UUID): _description_
            pagination (Pagination): _description_
            uow (IUnitOfWork): _description_

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            exception: _description_

        Returns:
            list[CommentInDB] | None:
        """
        try:
            if not await self._is_teaching_course(
                course_lecturer_id=course_lecturer_id,
                lecturer_id=lecturer_id,
                uow=uow,
            ):
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            return await self._get_comments_for_post(
                post_id=post_id,
                pagination=pagination,
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def get_own_comments_for_lecturer(
        self,
        post_id: UUID,
        course_lecturer_id: UUID,
        lecturer_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[CommentInDBExtended] | None:
        """Get comments written by lecturer

        Args:
            post_id (UUID):
            course_lecturer_id (UUID):
            lecturer_id (UUID):
            pagination (Pagination):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            exception:

        Returns:
            list[CommentInDBExtended] | None
        """
        try:
            if not await self._is_teaching_course(
                course_lecturer_id=course_lecturer_id,
                lecturer_id=lecturer_id,
                uow=uow,
            ):
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            return await self._get_comments_for_post_by_lecturer(
                post_id=post_id,
                lecturer_id=lecturer_id,
                pagination=pagination,
                uow=uow,
            )
        except Exception as exception:
            raise exception

    async def get_comments_for_post_by_student(
        self,
        post_id: UUID,
        enrolled_course_id: UUID,
        student_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[CommentInDBExtended] | None:
        """Get comments for post (Student can use this method)


        Args:
            post_id (UUID):
            enrolled_course_id (UUID):
            student_id (UUID):
            pagination (Pagination):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: STUDENT_NOT_ENROLLED_IN_COURSE
            ExceptionNotAcceptable406: STUDENT_BANNED_FROM_COURSE
            exception:

        Returns:
            list[CommentInDBExtended] | None
        """
        try:
            enrolled_course: EnrolledCourseInDB | None = (
                await self._get_enrolled_course(
                    enrolled_course_id=enrolled_course_id,
                    student_id=student_id,
                    uow=uow,
                )
            )
            if not enrolled_course:
                raise ExceptionNotFound404(
                    detail=ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE
                )

            if enrolled_course.is_banned:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.STUDENT_BANNED_FROM_COURSE
                )

            return await self._get_comments_for_post(
                post_id=post_id,
                pagination=pagination,
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def get_own_comments_for_student(
        self,
        post_id: UUID,
        enrolled_course_id: UUID,
        student_id: UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[CommentInDBExtended] | None:
        """Get comments written by student

        Args:
            post_id (UUID):
            enrolled_course_id (UUID):
            student_id (UUID):
            pagination (Pagination):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: STUDENT_NOT_ENROLLED_IN_COURSE
            ExceptionNotAcceptable406: STUDENT_BANNED_FROM_COURSE
            exception:

        Returns:
            list[CommentInDBExtended] | None
        """
        try:
            enrolled_course: EnrolledCourseInDB | None = (
                await self._get_enrolled_course(
                    enrolled_course_id=enrolled_course_id,
                    student_id=student_id,
                    uow=uow,
                )
            )
            if not enrolled_course:
                raise ExceptionNotFound404(
                    detail=ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE
                )

            if enrolled_course.is_banned:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.STUDENT_BANNED_FROM_COURSE
                )

            return await self._get_comments_for_post_by_student(
                post_id=post_id,
                student_id=student_id,
                pagination=pagination,
                uow=uow,
            )
        except Exception as exception:
            raise exception

    async def add_comment_for_lecturer(
        self,
        body: str,
        post_id: UUID,
        course_lecturer_id: UUID,
        lecturer_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        """add comment by lecturer

        Args:
            body (str):
            post_id (UUID):
            course_lecturer_id (UUID):
            lecturer_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: LECTURER_NOT_TEACHING_COURSE
            ExceptionNotFound404: POST_NOT_FOUND
            exception: otherwise
        """
        try:
            if not await self._is_teaching_course(
                course_lecturer_id=course_lecturer_id,
                lecturer_id=lecturer_id,
                uow=uow,
            ):
                raise ExceptionNotFound404(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            if not await self._is_post_exists(
                post_id=post_id,
                uow=uow,
            ):
                raise ExceptionNotFound404(detail=ErrorCode.POST_NOT_FOUND)

            comment_create = CommentCreate(
                post_id=post_id,
                body=body,
                author_type=AuthorType.lecturer,
                lecturer_id=lecturer_id,
                student_id=None,
            )

            await self._add_comment(
                comment_data=comment_create.model_dump(),
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def add_comment_for_student(
        self,
        body: str,
        post_id: UUID,
        enrolled_course_id: UUID,
        student_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        """add comment by lecturer

        Args:
            body (str):
            post_id (UUID):
            enrolled_course_id (UUID):
            student_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: STUDENT_NOT_ENROLLED_IN_COURSE
            ExceptionNotAcceptable406: STUDENT_BANNED_FROM_COURSE
            ExceptionNotFound404: POST_NOT_FOUND
            exception:
        """
        try:
            enrolled_course: EnrolledCourseInDB | None = (
                await self._get_enrolled_course(
                    enrolled_course_id=enrolled_course_id,
                    student_id=student_id,
                    uow=uow,
                )
            )
            if not enrolled_course:
                raise ExceptionNotFound404(
                    detail=ErrorCode.STUDENT_NOT_ENROLLED_IN_COURSE
                )

            if enrolled_course.is_banned:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.STUDENT_BANNED_FROM_COURSE
                )

            if not await self._is_post_exists(
                post_id=post_id,
                uow=uow,
            ):
                raise ExceptionNotFound404(detail=ErrorCode.POST_NOT_FOUND)

            comment_create = CommentCreate(
                post_id=post_id,
                body=body,
                author_type=AuthorType.student,
                student_id=student_id,
                lecturer_id=None,
            )

            await self._add_comment(
                comment_data=comment_create.model_dump(),
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def update_comment_for_lecturer(
        self,
        comment_id: UUID,
        lecturer_id: UUID,
        body: str,
        uow: IUnitOfWork,
    ) -> None:
        """update comment written by lecturer

        Args:
            comment_id (UUID):
            lecturer_id (UUID):
            body (str):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: COMMENT_NOT_FOUND
            exception:

        Returns:
            _type_: None
        """
        try:
            comment: CommentInDB | None = await self._get_comment_for_lecturer(
                comment_id=comment_id,
                lecturer_id=lecturer_id,
                uow=uow,
            )
            if not comment:
                raise ExceptionNotFound404(detail=ErrorCode.COMMENT_NOT_FOUND)

            if comment.body == body:
                return None

            await self._update_comment(
                comment_data={"body": body},
                comment_id=comment_id,
                uow=uow,
            )

            return None

        except Exception as exception:
            raise exception

    async def update_comment_for_student(
        self,
        comment_id: UUID,
        student_id: UUID,
        body: str,
        uow: IUnitOfWork,
    ) -> None:
        """update comment written by lecturer

        Args:
            comment_id (UUID):
            student_id (UUID):
            body (str):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: COMMENT_NOT_FOUND
            exception:

        Returns:
            _type_: None
        """
        try:
            comment: CommentInDB | None = await self._get_comment_for_student(
                comment_id=comment_id,
                student_id=student_id,
                uow=uow,
            )
            if not comment:
                raise ExceptionNotFound404(detail=ErrorCode.COMMENT_NOT_FOUND)

            if comment.body == body:
                return None

            await self._update_comment(
                comment_data={"body": body},
                comment_id=comment_id,
                uow=uow,
            )

            return None

        except Exception as exception:
            raise exception

    async def delete_comment_for_lecturer(
        self,
        comment_id: UUID,
        lecturer_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        """delete comment written by lecturer

        Args:
            comment_id (UUID):
            lecturer_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: COMMENT_NOT_FOUND
            exception:

        Returns:
            _type_: None
        """
        try:
            comment: CommentInDB | None = await self._get_comment_for_lecturer(
                comment_id=comment_id,
                lecturer_id=lecturer_id,
                uow=uow,
            )
            if not comment:
                raise ExceptionNotFound404(detail=ErrorCode.COMMENT_NOT_FOUND)

            await self._delete_comment(
                comment_id=comment_id,
                uow=uow,
            )

            return None

        except Exception as exception:
            raise exception

    async def delete_comment_for_student(
        self,
        comment_id: UUID,
        student_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        """delete comment written by lecturer

        Args:
            comment_id (UUID):
            student_id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: COMMENT_NOT_FOUND
            exception:

        Returns:
            _type_: None
        """
        try:
            comment: CommentInDB | None = await self._get_comment_for_student(
                comment_id=comment_id,
                student_id=student_id,
                uow=uow,
            )
            if not comment:
                raise ExceptionNotFound404(detail=ErrorCode.COMMENT_NOT_FOUND)

            await self._delete_comment(
                comment_id=comment_id,
                uow=uow,
            )

            return None

        except Exception as exception:
            raise exception

    async def _is_teaching_course(
        self,
        course_lecturer_id: UUID,
        lecturer_id: UUID,
        uow: IUnitOfWork,
    ) -> bool:
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    course_lecturer_id=course_lecturer_id,
                    lecturer_id=lecturer_id,
                    uow=uow,
                )
            )
            if course_lecturer is None:
                return False

            return True

        except Exception as exception:
            raise exception

    async def _is_post_exists(
        self,
        post_id: UUID,
        uow: IUnitOfWork,
    ) -> bool:
        try:
            post: PostInDB | None = await self._get_post(
                post_id=post_id,
                uow=uow,
            )
            if post is None:
                return False

            return True

        except Exception as exception:
            raise exception
