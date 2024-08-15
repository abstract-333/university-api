from models.enrolled_course import EnrolledCoursesOrm
from .base import BaseModelView


class EnrolledCourseAdmin(BaseModelView, model=EnrolledCoursesOrm):
    name = "Enrolled Course"
    name_plural = "Enrolled Courses"
    icon = "fas fa-business-time"
    pk_columns = [EnrolledCoursesOrm.id]
    form_ajax_refs = {
        "student": {
            "fields": ("id",),
            "order_by": "id",
        },
        "course": {
            "fields": ("id",),
            "order_by": "id",
        },
        "quizzes_results": {
            "fields": ("enrolled_course_id",),
            "order_by": "enrolled_course_id",
        },
    }

    column_list = [
        EnrolledCoursesOrm.id,
        EnrolledCoursesOrm.student,
        EnrolledCoursesOrm.course,
        EnrolledCoursesOrm.is_banned,
    ]
    form_columns = [
        EnrolledCoursesOrm.student_id,
        EnrolledCoursesOrm.taught_course_id,
    ]
