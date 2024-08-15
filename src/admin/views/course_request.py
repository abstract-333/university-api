from models.course_request import CoursesRequestsOrm
from .base import BaseModelView, get_datetime


class CourseRequestAdmin(BaseModelView, model=CoursesRequestsOrm):
    name = "Course Request"
    name_plural = "Courses Requests"
    icon = "fa-solid fa-people-arrows-left-right"

    pk_columns = [CoursesRequestsOrm.id]

    form_ajax_refs = {
        "student": {
            "fields": ("id",),
            "order_by": "id",
        },
        "processed_by_user": {
            "fields": ("id",),
            "order_by": "id",
        },
        "course": {
            "fields": ("id",),
            "order_by": "id",
        },
    }

    column_formatters = get_datetime(CoursesRequestsOrm)
    column_formatters_detail = get_datetime(CoursesRequestsOrm)
    column_list = [
        CoursesRequestsOrm.student,
        CoursesRequestsOrm.course,
        CoursesRequestsOrm.description,
        CoursesRequestsOrm.is_accepted,
        CoursesRequestsOrm.processed_at,
        CoursesRequestsOrm.processed_by_user,
        CoursesRequestsOrm.added_at,
        CoursesRequestsOrm.updated_at,
    ]
    column_searchable_list = [
        CoursesRequestsOrm.student_id,
        CoursesRequestsOrm.taught_course_id,
        CoursesRequestsOrm.description,
    ]
    column_details_list = [
        CoursesRequestsOrm.course,
        CoursesRequestsOrm.student,
        CoursesRequestsOrm.student_id,
        CoursesRequestsOrm.taught_course_id,
        CoursesRequestsOrm.description,
        CoursesRequestsOrm.is_accepted,
        CoursesRequestsOrm.processed_at,
        CoursesRequestsOrm.processed_by,
        CoursesRequestsOrm.processed_by_user,
    ]
    form_columns = [
        CoursesRequestsOrm.student_id,
        CoursesRequestsOrm.taught_course_id,
        CoursesRequestsOrm.description,
        CoursesRequestsOrm.processed_at,
        CoursesRequestsOrm.is_accepted,
        CoursesRequestsOrm.processed_by,
    ]
