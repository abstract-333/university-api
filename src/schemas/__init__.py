from .auth import AccessRefreshTokens
from .comment import CommentCreate, CommentInDBExtended, CommentUpdate
from .course_lecturer import (
    CourseLecturerInDB,
    CourseLecturerUpdate,
    CourseLecturerCreate,
    CourseLecturerInDBExtended,
)
from .course import CourseInDB, CourseCreate
from .course_request import (
    CourseRequestInDBExtended,
    CourseRequestInDBExtendedStudent,
    CourseRequestInDB,
    CourseRequestCreate,
    CourseRequestUpdate,
)
from .enrolled_course import (
    EnrolledCourseCreate,
    EnrolledCourseInDBExtended,
    EnrolledCourseUpdate,
)
from .faculty import Faculty
from .file import FileInDB, FileCreate, FileUpdate
from .lecture import LectureInDB, LectureCreate, LecturetUpdate
from .lecturer import LecturerInDB, LecturerCreate
from .lecturer_request import (
    LecturerRequestInDB,
    LecturerRequestCreate,
    LecturerRequestUpdate,
    LecturerRequestProcessUpdate,
    LecturerRequestProcess,
)
from .post import PostInDB, PostCreate, PostUpdate, PostInDBExtended
from .question import QuestionCreate, QuestionInDB, QuestionUpdate, QuestionInDBExtended
from .quiz import QuizCreate, QuizUpdate, QuizInDB
from .quiz_result import QuizResultCreate, QuizResultInDB, QuizResultUpdate
from .speciality import SpecialityInDB, SpecialityCreate
from .speciality_course import (
    SpecialityCourseInDBExtended,
    SpecialityCourseCreate,
    SpecialityCourseInDB,
)
from .student import (
    StudentInDBWithSpeciality,
    StudentUpdate,
    StudentCreate,
    StudentUpdateState,
    StudentComment,
)
from .taught_course import (
    TaughtCourseInDB,
    TaughtCourseCreate,
    TaughtCourseUpdate,
    TaughtCourseInDBExtended,
    TaughtCourseInDBSpecliatyCourse,
)
from .user import (
    UserRead,
    UserCreate,
    BaseUser,
    UserHashedPassword,
    UserReadWithPassword,
    UserUpdate,
)
from .active_session import (
    ActiveSessionCreate,
    ActiveSessionInDB,
    ActiveSessionUpdate,
    ActiveSessionOutput,
)
