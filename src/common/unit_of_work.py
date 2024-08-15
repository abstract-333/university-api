from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from respository import (
    UserRepository,
    StudentRepository,
    FacultyRepository,
    LecturerRepository,
    SpecialityRepository,
    FacultyRepositoryBase,
    UserRepositoryBase,
    QuizResultBaseRepository,
    QuizResultRepository,
    SpecialityRepositoryBase,
    StudentRepositoryBase,
    LecturerRepositoryBase,
    ActiveSessionRepository,
    ActiveSessionRepositoryBase,
    CommentRepositoryBase,
    CommentRepository,
    LecturerRequestRepository,
    LectureRepositoryBase,
    LectureRepository,
    PostRepositoryBase,
    QuestionRepository,
    QuestionsRepositoryBase,
    PostRepository,
    LecturerRequestRepositoryBase,
    TaughtCourseRepositoryBase,
    TaughtCourseRepository,
    QuizBaseRepository,
    QuizRepository,
    SpecialityCourseRepository,
    SpecialityCourseRepositoryBase,
    CourseLecturerRepository,
    CourseLecturerRepositoryBase,
    CourseRequestRepositoryBase,
    CourseRequestRepository,
    EnrolledCourseRepsitory,
    EnrolledCourseRepsitoryBase,
    FileRepository,
    FileRepositoryBase,
)
from storage import AsyncSessionFactory


class IUnitOfWork(ABC):
    user: UserRepositoryBase
    student: StudentRepositoryBase
    faculty: FacultyRepositoryBase
    lecturer: LecturerRepositoryBase
    speciality: SpecialityRepositoryBase
    lecturer_request: LecturerRequestRepositoryBase
    active_session: ActiveSessionRepositoryBase
    taught_course: TaughtCourseRepositoryBase
    speciality_course: SpecialityCourseRepositoryBase
    course_lecturer: CourseLecturerRepositoryBase
    course_request: CourseRequestRepositoryBase
    enrolled_course: EnrolledCourseRepsitoryBase
    post: PostRepositoryBase
    comment: CommentRepositoryBase
    lecture: LectureRepositoryBase
    file: FileRepositoryBase
    question: QuestionsRepositoryBase
    quiz: QuizBaseRepository
    quiz_result: QuizResultBaseRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = AsyncSessionFactory().get_async_session_maker()

    async def __aenter__(self) -> None:
        self.session: AsyncSession = self.session_factory()

        self.user = UserRepository(session=self.session)
        self.student = StudentRepository(session=self.session)
        self.faculty = FacultyRepository(session=self.session)
        self.lecturer = LecturerRepository(session=self.session)
        self.speciality = SpecialityRepository(session=self.session)
        self.lecturer_request = LecturerRequestRepository(session=self.session)
        self.active_session = ActiveSessionRepository(session=self.session)
        self.taught_course = TaughtCourseRepository(session=self.session)
        self.speciality_course = SpecialityCourseRepository(session=self.session)
        self.course_lecturer = CourseLecturerRepository(session=self.session)
        self.course_request = CourseRequestRepository(session=self.session)
        self.enrolled_course = EnrolledCourseRepsitory(session=self.session)
        self.post = PostRepository(session=self.session)
        self.comment = CommentRepository(session=self.session)
        self.lecture = LectureRepository(session=self.session)
        self.file = FileRepository(session=self.session)
        self.question = QuestionRepository(session=self.session)
        self.quiz = QuizRepository(session=self.session)
        self.quiz_result = QuizResultRepository(session=self.session)

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
