from models import LecturersOrm
from .base import BaseModelView


class LecturerAdmin(BaseModelView, model=LecturersOrm):
    name = "Lecturer"
    name_plural = "Lecturers"
    icon = "fa-solid fa-chalkboard-teacher"
    pk_columns = [LecturersOrm.id]

    form_ajax_refs = {
        "user": {
            "fields": ("id",),
            "order_by": "id",
        },
        "faculty": {
            "fields": ("name",),
            "order_by": "name",
        },
        "taught_courses": {
            "fields": ("lecturer_id",),
            "order_by": "lecturer_id",
        },
        "comments": {
            "fields": ("lecturer_id",),
            "order_by": "lecturer_id",
        },
    }

    column_list = [
        LecturersOrm.user,
        LecturersOrm.faculty_name,
        LecturersOrm.is_approved,
    ]
    column_searchable_list = [LecturersOrm.user_id, LecturersOrm.faculty_name]
    form_excluded_columns = [
        LecturersOrm.faculty,
        LecturersOrm.user,
        LecturersOrm.id,
        LecturersOrm.taught_courses,
        LecturersOrm.comments,
    ]
