from typing import Any

from fastapi import APIRouter

from admin import (
    UserAdmin,
    StudentAdmin,
    LecturerAdmin,
    CourseAdmin,
    TaughtCourseAdmin,
    CourseLecturerAdmin,
    SpecialityCourseAdmin,
    EnrolledCourseAdmin,
    PostAdmin,
    CommentAdmin,
    FileAdmin,
    FacultyAdmin,
    SpecialityAdmin,
    LectureAdmin,
    QuestionAdmin,
    QuizAdmin,
    QuizResultAdmin,
    LecturerRequestAdmin,
    CourseRequestAdmin,
    ActiveSessionAdmin,
)
from api import (
    auth_router,
    comment_student_router,
    user_router,
    student_router,
    lecturer_router,
    post_lecturer_router,
    enrolled_course_student_router,
    faculty_router,
    quiz_student_router,
    taught_course_student_router,
    quiz_result_student_router,
    lecture_student_router,
    speciality_router,
    quiz_lecturer_router,
    quiz_result_lecturer_router,
    question_lecturer_router,
    post_student_router,
    health_router,
    file_student_router,
    lecturer_request_router,
    lecture_lecturer_router,
    session_router,
    speciality_course_student_router,
    taught_course_admin_router,
    lecturer_request_admin_router,
    course_request_student_router,
    course_request_lecturer_router,
    taught_course_lecturer_router,
    speciality_course_lecturer_router,
    course_lecturer_router,
    comment_lecturer_router,
    file_lecturer_router,
)

routers: list[APIRouter] = [
    auth_router,
    user_router,
    student_router,
    lecturer_router,
    enrolled_course_student_router,
    lecturer_request_router,
    lecturer_request_admin_router,
    course_lecturer_router,
    file_lecturer_router,
    file_student_router,
    lecture_student_router,
    lecture_lecturer_router,
    post_lecturer_router,
    post_student_router,
    comment_lecturer_router,
    comment_student_router,
    question_lecturer_router,
    taught_course_lecturer_router,
    taught_course_student_router,
    taught_course_admin_router,
    quiz_lecturer_router,
    quiz_student_router,
    quiz_result_student_router,
    quiz_result_lecturer_router,
    course_request_student_router,
    course_request_lecturer_router,
    faculty_router,
    speciality_router,
    speciality_course_lecturer_router,
    speciality_course_student_router,
    session_router,
    health_router,
]

views: list[Any] = [
    UserAdmin,
    StudentAdmin,
    LecturerAdmin,
    CourseAdmin,
    TaughtCourseAdmin,
    CourseLecturerAdmin,
    SpecialityCourseAdmin,
    EnrolledCourseAdmin,
    PostAdmin,
    CommentAdmin,
    FileAdmin,
    LectureAdmin,
    QuestionAdmin,
    QuizAdmin,
    QuizResultAdmin,
    LecturerRequestAdmin,
    CourseRequestAdmin,
    FacultyAdmin,
    SpecialityAdmin,
    ActiveSessionAdmin,
]
