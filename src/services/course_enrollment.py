import uuid

from common.unit_of_work import IUnitOfWork
from exception.base import (
    ExceptionBadRequest400,
    ExceptionMethodNotAllowed405,
    ExceptionNotAcceptable406,
    ExceptionNotFound404,
)
from exception.error_code import ErrorCode
from schemas.course_lecturer import CourseLecturerInDB
from schemas.course_request import (
    CourseRequestBase,
    CourseRequestCreate,
    CourseRequestInDB,
    CourseRequestInDBExtended,
    CourseRequestInDBExtendedStudent,
    CourseRequestProcess,
    CourseRequestUpdate,
)
from schemas.enrolled_course import (
    EnrolledCourseCreate,
    EnrolledCourseInDB,
    EnrolledCourseInDBExtended,
)
from schemas.pagination import Pagination
from specification.course_lecturer import (
    CourseLecturerCourseIDSpecification,
    CourseLecturerLecturerIdSpecification,
)
from specification.course_request import (
    CourseRequestCourseIdSpecification,
    CourseRequestIdSpecification,
    CourseRequestIsProcessedSpecification,
    CourseRequestStudentIdSpecification,
)
from specification.enrolled_course import (
    EnrolledCourseCourseIdSpecification,
    EnrolledCourseStudentIdSpecification,
)
from specification.student import StudentIsFreshmanSpecification


class CourseEnrollmentService:
    @classmethod
    async def _get_all_unprocessed_course_requests_for_student(
        cls,
        student_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[CourseRequestInDBExtended] | None:
        async with uow:
            course_requests: list[
                CourseRequestInDBExtended
            ] | None = await uow.course_request.get_course_requests_extended_course_processed_by(
                specification=~CourseRequestIsProcessedSpecification()
                & CourseRequestStudentIdSpecification(student_id=student_id),
                pagination=pagination,
            )
            return course_requests

    @classmethod
    async def _get_all_unprocessed_course_requests_for_course(
        cls,
        course_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[CourseRequestInDBExtendedStudent] | None:
        async with uow:
            return await uow.course_request.get_course_requests_extended_student(
                specification=CourseRequestCourseIdSpecification(course_id=course_id)
                & ~CourseRequestIsProcessedSpecification(),
                pagination=pagination,
            )

    @classmethod
    async def _get_unprocessed_course_request_freshman(
        cls,
        course_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[CourseRequestInDBExtendedStudent] | None:
        async with uow:
            return await uow.course_request.get_course_requests_extended_student(
                specification=StudentIsFreshmanSpecification(is_freshman=True)
                & CourseRequestCourseIdSpecification(course_id=course_id)
                & ~CourseRequestIsProcessedSpecification(),
                pagination=pagination,
            )

    @classmethod
    async def _get_unprocessed_course_request(
        cls,
        student_id: uuid.UUID,
        course_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> CourseRequestInDB | None:
        async with uow:
            specification = (
                CourseRequestStudentIdSpecification(student_id=student_id)
                & CourseRequestCourseIdSpecification(course_id=course_id)
                & ~CourseRequestIsProcessedSpecification()
            )

            course_request: CourseRequestInDB | None = (
                await uow.course_request.get_course_request(specification=specification)
            )
            return course_request

    @classmethod
    async def _get_course_lecturer(
        cls,
        lecturer_id: uuid.UUID,
        course_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> CourseLecturerInDB | None:
        async with uow:
            return await uow.course_lecturer.get_course_lecturer(
                specification=CourseLecturerCourseIDSpecification(course_id=course_id)
                & CourseLecturerLecturerIdSpecification(lecturer_id=lecturer_id)
            )

    @classmethod
    async def _get_enrolled_course(
        cls,
        course_id: uuid.UUID,
        student_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> EnrolledCourseInDB | None:
        async with uow:
            enrolled_course: EnrolledCourseInDB | None = (
                await uow.enrolled_course.get_enrolled_course(
                    specification=EnrolledCourseCourseIdSpecification(
                        course_id=course_id
                    )
                    & EnrolledCourseStudentIdSpecification(student_id=student_id)
                )
            )
            return enrolled_course

    @classmethod
    async def _get_enrolled_courses(
        cls,
        student_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[EnrolledCourseInDBExtended] | None:
        async with uow:
            enrolled_course: list[
                EnrolledCourseInDBExtended
            ] | None = await uow.enrolled_course.get_enrolled_courses(
                specification=EnrolledCourseStudentIdSpecification(
                    student_id=student_id
                ),
                pagination=pagination,
            )
            return enrolled_course

    @classmethod
    async def _get_unprocessed_course_request_by_student(
        cls,
        student_id: uuid.UUID,
        request_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> CourseRequestInDB | None:
        async with uow:
            course_request: CourseRequestInDB | None = (
                await uow.course_request.get_course_request(
                    specification=CourseRequestStudentIdSpecification(
                        student_id=student_id
                    )
                    & CourseRequestIdSpecification(id=request_id)
                    & ~CourseRequestIsProcessedSpecification(),
                )
            )
            return course_request

    @classmethod
    async def _get_course_request_by_course_student_id(
        cls,
        student_id: uuid.UUID,
        course_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> CourseRequestInDB | None:
        async with uow:
            Course: CourseRequestInDB | None = (
                await uow.course_request.get_course_request(
                    specification=CourseRequestStudentIdSpecification(
                        student_id=student_id
                    )
                    & CourseRequestCourseIdSpecification(course_id=course_id)
                )
            )
            return Course

    @classmethod
    async def _add_course_request(
        cls,
        course_request_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.course_request.add_course_request(
                course_request_data=course_request_data,
            )
            await uow.commit()

    @classmethod
    async def _edit_course_request(
        cls,
        course_request_data: dict,
        request_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.course_request.edit_course_request(
                course_request_data=course_request_data,
                specification=CourseRequestIdSpecification(id=request_id)
                & ~CourseRequestIsProcessedSpecification(),
            )
            await uow.commit()

    @classmethod
    async def _accept_request_register_student_in_course(
        cls,
        course_request_data: dict,
        enrolled_course_data: dict,
        request_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.course_request.edit_course_request(
                course_request_data=course_request_data,
                specification=CourseRequestIdSpecification(id=request_id)
                & ~CourseRequestIsProcessedSpecification(),
            )
            await uow.enrolled_course.add_enrolled_course(
                enrolled_course_data=enrolled_course_data
            )

            await uow.commit()

    async def get_all_course_requests_for_course(
        self,
        course_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> list[CourseRequestInDBExtendedStudent] | None:
        """Return all course requests for course

        Args:
            course_id (uuid.UUID): taught_course_id
            lecturer_id (uuid.UUID): Who make the request, must teaching the course
            uow (IUnitOfWork):
            pagination (Pagination):

        Raises:
            ExceptionMethodNotAllowed405: LECTURER_NOT_TEACHING_COURSE

        Returns:
            list[CourseRequestInDBExtendedStudent] | None
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    lecturer_id=lecturer_id, course_id=course_id, uow=uow
                )
            )

            if course_lecturer is None:
                raise ExceptionMethodNotAllowed405(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            return await self._get_all_unprocessed_course_requests_for_course(
                course_id=course_id,
                pagination=pagination,
                uow=uow,
            )

        except Exception as exception:
            raise exception

    async def accept_course_request(
        self,
        course_request_id: uuid.UUID,
        course_id: uuid.UUID,
        student_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        lecturer_user_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        """accept course request

        Args:
            course_request_id (uuid.UUID): _description_
            course_id (uuid.UUID): _description_
            student_id (uuid.UUID): _description_
            lecturer_id (uuid.UUID): _description_
            lecturer_user_id (uuid.UUID): _description_
            uow (IUnitOfWork): _description_

        Raises:
            ExceptionMethodNotAllowed405: LECTURER_NOT_TEACHING_COURSE

            ExceptionBadRequest400: STUDENT_ALREADY_ENROLLED_IN_COURSE

            ExceptionNotFound404: COURSE_REQUEST_NOT_EXISTS

            exception:

        Returns:
            _type_: None
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    lecturer_id=lecturer_id,
                    course_id=course_id,
                    uow=uow,
                )
            )

            if course_lecturer is None:
                raise ExceptionMethodNotAllowed405(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            student_already_registered: EnrolledCourseInDB | None = (
                await self._get_enrolled_course(
                    course_id=course_id,
                    student_id=student_id,
                    uow=uow,
                )
            )
            course_request: CourseRequestInDB | None = (
                await self._get_unprocessed_course_request_by_student(
                    student_id=student_id,
                    request_id=course_request_id,
                    uow=uow,
                )
            )

            if course_request is None:
                raise ExceptionNotFound404(detail=ErrorCode.COURSE_REQUEST_NOT_EXISTS)

            if student_already_registered is not None:
                raise ExceptionBadRequest400(
                    detail=ErrorCode.STUDENT_ALREADY_ENROLLED_IN_COURSE
                )

            coures_requesta_process = CourseRequestProcess(
                is_accepted=True,
                processed_by=lecturer_user_id,
            )
            enrolled_course = EnrolledCourseCreate(
                student_id=student_id,
                taught_course_id=course_id,
            )

            await self._accept_request_register_student_in_course(
                course_request_data=coures_requesta_process.model_dump(),
                enrolled_course_data=enrolled_course.model_dump(),
                request_id=course_request.id,
                uow=uow,
            )

            return None

        except Exception as exception:
            raise exception

    async def reject_course_request(
        self,
        course_request_id: uuid.UUID,
        course_id: uuid.UUID,
        student_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        lecturer_user_id: uuid.UUID,
        uow: IUnitOfWork,
    ) -> None:
        """reject course request

        Args:
            course_request_id (uuid.UUID): _description_
            course_id (uuid.UUID): _description_
            student_id (uuid.UUID): _description_
            lecturer_id (uuid.UUID): _description_
            lecturer_user_id (uuid.UUID): _description_
            uow (IUnitOfWork): _description_

        Raises:
            ExceptionMethodNotAllowed405: LECTURER_NOT_TEACHING_COURSE

            ExceptionBadRequest400: STUDENT_ALREADY_ENROLLED_IN_COURSE

            ExceptionNotFound404: COURSE_REQUEST_NOT_EXISTS

            exception:

        Returns:
            _type_: None
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    lecturer_id=lecturer_id,
                    course_id=course_id,
                    uow=uow,
                )
            )

            if course_lecturer is None:
                raise ExceptionMethodNotAllowed405(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )

            student_already_registered: EnrolledCourseInDB | None = (
                await self._get_enrolled_course(
                    course_id=course_id,
                    student_id=student_id,
                    uow=uow,
                )
            )

            course_request: CourseRequestInDB | None = (
                await self._get_unprocessed_course_request_by_student(
                    student_id=student_id,
                    request_id=course_request_id,
                    uow=uow,
                )
            )

            if course_request is None:
                raise ExceptionNotFound404(detail=ErrorCode.COURSE_REQUEST_NOT_EXISTS)

            if student_already_registered is not None:
                raise ExceptionBadRequest400(
                    detail=ErrorCode.STUDENT_ALREADY_ENROLLED_IN_COURSE
                )

            coures_requesta_process = CourseRequestProcess(
                is_accepted=False,
                processed_by=lecturer_user_id,
            )
            enrolled_course = EnrolledCourseCreate(
                student_id=student_id,
                taught_course_id=course_id,
            )

            await self._accept_request_register_student_in_course(
                course_request_data=coures_requesta_process.model_dump(),
                enrolled_course_data=enrolled_course.model_dump(),
                request_id=course_request.id,
                uow=uow,
            )

            return None

        except Exception as exception:
            raise exception

    async def accept_course_requests_freshman(
        self,
        course_id: uuid.UUID,
        lecturer_id: uuid.UUID,
        lecturer_user_id: uuid.UUID,
        uow: IUnitOfWork,
        pagination: Pagination,
    ) -> None:
        """_summary_

        Args:
            course_id (uuid.UUID): taught_course_id

            lecturer_id (uuid.UUID): lecturer_id

            lecturer_user_id (uuid.UUID): user_id of the lecturer

            uow (IUnitOfWork):

            pagination (Pagination):

        Raises:
            ExceptionMethodNotAllowed405: LECTURER_NOT_TEACHING_COURSE

            exception:

        Returns:
            None
        """
        try:
            course_lecturer: CourseLecturerInDB | None = (
                await self._get_course_lecturer(
                    lecturer_id=lecturer_id, course_id=course_id, uow=uow
                )
            )

            if course_lecturer is None:
                raise ExceptionMethodNotAllowed405(
                    detail=ErrorCode.LECTURER_NOT_TEACHING_COURSE
                )
            course_request_freshman: list[
                CourseRequestInDBExtendedStudent
            ] | None = await self._get_unprocessed_course_request_freshman(
                course_id=course_id,
                uow=uow,
                pagination=pagination,
            )
            if course_request_freshman is None:
                return None

            for course_request in course_request_freshman:
                student_already_registered: EnrolledCourseInDB | None = (
                    await self._get_enrolled_course(
                        course_id=course_id,
                        student_id=course_request.student.id,
                        uow=uow,
                    )
                )

                if student_already_registered is not None:
                    continue

                coures_requesta_process = CourseRequestProcess(
                    is_accepted=True,
                    processed_by=lecturer_user_id,
                )
                enrolled_course = EnrolledCourseCreate(
                    student_id=course_request.student.id,
                    taught_course_id=course_id,
                )
                await self._accept_request_register_student_in_course(
                    course_request_data=coures_requesta_process.model_dump(),
                    enrolled_course_data=enrolled_course.model_dump(),
                    request_id=course_request.id,
                    uow=uow,
                )

            return None

        except Exception as exception:
            raise exception

    async def get_all_course_requests_for_student(
        self,
        student_id: uuid.UUID,
        pagination: Pagination,
        uow: IUnitOfWork,
    ) -> list[CourseRequestInDBExtended] | None:
        """
            Return all unprocessed course requests that student has sent

        Args:
            student_id (uuid.UUID)

            pagination (Pagination)

            uow (IUnitOfWork)

        Raises:
            e

        Returns:
            list[CourseRequestInDBExtended] | None
        """
        try:
            course_requests: list[
                CourseRequestInDBExtended
            ] | None = await self._get_all_unprocessed_course_requests_for_student(
                student_id=student_id,
                pagination=pagination,
                uow=uow,
            )
            return course_requests

        except Exception as e:
            raise e

    async def add_course_request(
        self,
        student_id: uuid.UUID,
        course_request_create: CourseRequestBase,
        uow: IUnitOfWork,
    ) -> None:
        """Add course request if another one didn't exists for current course and student

        Args:
            student_id (uuid.UUID)

            course_request_create (CourseRequestBase)

            uow (IUnitOfWork)

        Raises:
            ExceptionNotAcceptable406: STUDENT_ALREADY_ENROLLED_IN_COURSE

            ExceptionNotAcceptable406: COURSE_REQUEST_ALREADY_SENT

        Returns:
            None
        """
        try:
            enrolled_course: EnrolledCourseInDB | None = (
                await self._get_enrolled_course(
                    course_id=course_request_create.taught_course_id,
                    student_id=student_id,
                    uow=uow,
                )
            )

            if enrolled_course is not None:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.STUDENT_ALREADY_ENROLLED_IN_COURSE
                )

            old_requests: CourseRequestInDB | None = (
                await self._get_unprocessed_course_request(
                    student_id=student_id,
                    course_id=course_request_create.taught_course_id,
                    uow=uow,
                )
            )
            if old_requests is not None:
                raise ExceptionNotAcceptable406(
                    detail=ErrorCode.COURSE_REQUEST_ALREADY_SENT
                )

            new_course_request = CourseRequestCreate(
                student_id=student_id,
                taught_course_id=course_request_create.taught_course_id,
                description=course_request_create.description,
            )

            await self._add_course_request(
                course_request_data=new_course_request.model_dump(), uow=uow
            )

            return None

        except Exception as e:
            raise e

    async def edit_course_request(
        self,
        course_id: uuid.UUID,
        student_id: uuid.UUID,
        course_request_update: CourseRequestUpdate,
        uow: IUnitOfWork,
    ) -> None:
        """Edit course request (only Description now)

        Args:
            course_id (uuid.UUID): taught_course_id

            student_id (uuid.UUID)

            course_request_update (CourseRequestUpdate)

            uow (IUnitOfWork)

        Raises:
            ExceptionNotFound404: COURSE_REQUEST_NOT_EXISTS (Maybe it's already processed or not exists at all)
            e: _description_

        Returns:
            _type_: _description_
        """
        try:
            old_request: CourseRequestInDB | None = (
                await self._get_unprocessed_course_request(
                    student_id=student_id,
                    course_id=course_id,
                    uow=uow,
                )
            )

            if old_request is None:
                raise ExceptionNotFound404(detail=ErrorCode.COURSE_REQUEST_NOT_EXISTS)

            if old_request != course_request_update:
                await self._edit_course_request(
                    course_request_data=course_request_update.model_dump(),
                    request_id=old_request.id,
                    uow=uow,
                )

            return None

        except Exception as e:
            raise e

    async def get_enrolled_courses(
        self, student_id: uuid.UUID, pagination: Pagination, uow: IUnitOfWork
    ) -> list[EnrolledCourseInDBExtended] | None:
        try:
            return await self._get_enrolled_courses(
                student_id=student_id,
                pagination=pagination,
                uow=uow,
            )

        except Exception as exception:
            raise exception
