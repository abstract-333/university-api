from typing import Any
from models import CoursesLecturersOrm
from .base import BaseModelView


class CourseLecturerAdmin(BaseModelView, model=CoursesLecturersOrm):
    name = "Course Lecturer"
    name_plural = "Courses Lecturers"
    icon = "fas fa-archive"
    pk_columns = [CoursesLecturersOrm.id]
    form_ajax_refs: dict[str, dict[Any, Any]] = {
        "lecturer": {
            "fields": ("id",),
            "order_by": "id",
        },
        "course": {
            "fields": ("id",),
            "order_by": "id",
        },
        "quizzes": {
            "fields": ("lecturer_course",),
            "order_by": "lecturer_course",
        },
        "questions": {
            "fields": ("lecturer_course",),
            "order_by": "lecturer_course",
        },
        "posts": {
            "fields": ("lecturer_course",),
            "order_by": "lecturer_course",
        },
        "lectures": {
            "fields": ("lecturer_course",),
            "order_by": "lecturer_course",
        },
    }
    column_list = [
        CoursesLecturersOrm.id,
        CoursesLecturersOrm.course,
        CoursesLecturersOrm.lecturer,
        CoursesLecturersOrm.posts,
        CoursesLecturersOrm.quizzes,
        CoursesLecturersOrm.questions,
        CoursesLecturersOrm.lectures,
    ]
    column_searchable_list = [
        CoursesLecturersOrm.lecturer,
    ]
    form_excluded_columns = [
        CoursesLecturersOrm.id,
        CoursesLecturersOrm.course,
        CoursesLecturersOrm.lecturer,
        CoursesLecturersOrm.posts,
        CoursesLecturersOrm.quizzes,
        CoursesLecturersOrm.questions,
        CoursesLecturersOrm.lectures,
    ]
