from .base import SQLAlchemyRepository, AbstractSQLRepository
from .faculty import FacultyRepository, FacultyRepositoryBase
from .lecturer import LecturerRepository, LecturerRepositoryBase
from .speciality import SpecialityRepository, SpecialityRepositoryBase
from .student import StudentRepository, StudentRepositoryBase
from .user import UserRepository, UserRepositoryBase
from .active_session import ActiveSessionRepository, ActiveSessionRepositoryBase
from .lecturer_request import LecturerRequestRepository, LecturerRequestRepositoryBase
from .taught_course import TaughtCourseRepository, TaughtCourseRepositoryBase
from .speciality_course import (
    SpecialityCourseRepositoryBase,
    SpecialityCourseRepository,
)
from .course_lecturer import CourseLecturerRepository, CourseLecturerRepositoryBase
from .course_request import CourseRequestRepositoryBase, CourseRequestRepository
from .enrolled_course import EnrolledCourseRepsitory, EnrolledCourseRepsitoryBase
from .post import PostRepository, PostRepositoryBase
from .comment import CommentRepositoryBase, CommentRepository
from .lecture import LectureRepositoryBase, LectureRepository
from .file import FileRepository, FileRepositoryBase
from .question import QuestionRepository, QuestionsRepositoryBase
from .quiz import QuizBaseRepository, QuizRepository
from .quiz_result import QuizResultBaseRepository, QuizResultRepository
