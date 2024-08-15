from specification.quiz import (
    QuizIdSpecification,
    QuizActiveSpecification,
    QuizLecturerCourseIdSpecification,
)
from .active_session import (
    SessionDeviceIdSpecification,
    SessionRefreshTokenSpecification,
    SessionUserIdSpecification,
    SessionIdSpecification,
)
from .base import SpecificationSQLAlchemy, Specification
from .comment import (
    CommentAuthorTypeSpecification,
    CommentLecturerIdSpecification,
    CommentPostIdSpecification,
    CommentStudentIdSpecification,
)
from .course_lecturer import (
    CourseLecturerCourseIDSpecification,
    CourseLecturerLecturerIdSpecification,
    CourseLecturerIdSpecification,
)
from .course_request import (
    CourseRequestCourseIdSpecification,
    CourseRequestIdSpecification,
    CourseRequestIsAcceptedSpecification,
    CourseRequestIsProcessedSpecification,
    CourseRequestStudentIdSpecification,
)
from .enrolled_course import (
    EnrolledCourseCourseIdSpecification,
    EnrolledCourseStudentIdSpecification,
    EnrolledCourseIdSpecification,
)
from .faculty import FacultyNameSpecification
from .file import FileIdSpecification, FileFileIdSpecification
from .lecturer import (
    LecturerUserIdSpecification,
    LecturerFacultySpecification,
    LecturerIdSpecification,
)
from .lecturer_request import (
    LecturerRequestIsAcceptedSpecification,
    LecturerRequestIsProcessedSpecification,
    LecturerRequestUserIdSpecification,
    LecturerRequestIdSpecification,
    LecturerRequestFacultySpecification,
)
from .post import PostCourseIdSpecification, PostIdSpecification
from .question import (
    QuestionLecturerCourseIdSpecification,
    QuestionIdSpecification,
    QuestionIsVisibleSpecification,
)
from .speciality import (
    SpecialityNameSpecification,
    SpecialityFacultySpecification,
    SpecialityIdSpecification,
)
from .speciality_course import (
    SpecialityCourseClassSpecification,
    SpecialityCourseIdSpecification,
    SpecialityCourseNameSpecification,
    SpecialityCourseSemesterSpecification,
    SpecialityCourseSpecialityIdSpecification,
)
from .student import (
    StudentUserIdSpecification,
    StudentIdSpecification,
    StudentIsFreshmanSpecification,
)
from .taught_course import (
    TaughtCourseYearSpecification,
    TaughtCourseSpecialityCourseIDSpecification,
    TaughtCourseIdSpecification,
)
from .user import UserEmailSpecification
from .quiz_result import (
    QuizResultEnrolledCourseIdSpecification,
    QuizResultIdSpecification,
    QuizResultQuizIdSpecification,
)

__all__ = (
    "QuizIdSpecification",
    "QuizActiveSpecification",
    "QuizLecturerCourseIdSpecification",
    "QuizResultEnrolledCourseIdSpecification",
    "QuizResultIdSpecification",
    "QuizResultQuizIdSpecification",
)
