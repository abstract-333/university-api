from models import TaughtCoursesOrm
from .base import BaseModelView, get_datetime


class TaughtCourseAdmin(BaseModelView, model=TaughtCoursesOrm):
    name = "Taught Course"
    name_plural = "Taught Courses"
    icon = "fas fa-book-reader"
    pk_columns = [TaughtCoursesOrm.id]
    column_formatters = get_datetime(TaughtCoursesOrm)
    column_formatters[TaughtCoursesOrm.description] = lambda m, a: (
        m.description if len(m.description) < 50 else m.description[:50] + "..."
    )
    column_formatters_detail = get_datetime(TaughtCoursesOrm)
    column_formatters_detail[TaughtCoursesOrm.description] = lambda m, a: (
        m.description if len(m.description) < 50 else m.description[:50] + "..."
    )
    form_ajax_refs = {
        "courses_lecturers": {
            "fields": ("course_id",),
            "order_by": "course_id",
        },
        "enrolled_courses": {
            "fields": ("taught_course_id",),
            "order_by": "taught_course_id",
        },
        "courses_requests": {
            "fields": ("taught_course_id",),
            "order_by": "taught_course_id",
        },
        "speciality_course": {
            "fields": ("id",),
            "order_by": "id",
        },
    }
    column_list = [
        TaughtCoursesOrm.description,
        TaughtCoursesOrm.speciality_course,
        TaughtCoursesOrm.year,
        TaughtCoursesOrm.added_at,
        TaughtCoursesOrm.updated_at,
    ]
    column_searchable_list = [
        TaughtCoursesOrm.description,
        TaughtCoursesOrm.year,
    ]
    form_columns = [
        TaughtCoursesOrm.description,
        TaughtCoursesOrm.year,
        TaughtCoursesOrm.speciality_course_id,
    ]
    column_default_sort = [("description", True)]
