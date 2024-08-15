from models import StudentsOrm
from .base import BaseModelView


class StudentAdmin(BaseModelView, model=StudentsOrm):
    name = "Student"
    name_plural = "Students"
    icon = "fa-solid fa-user-graduate"
    pk_columns = [StudentsOrm.id]
    column_list = [
        StudentsOrm.university_id,
        StudentsOrm.user,
        StudentsOrm.speciality,
        StudentsOrm.class_id,
        StudentsOrm.is_freshman,
    ]
    column_searchable_list = [
        StudentsOrm.university_id,
        StudentsOrm.user_id,
        StudentsOrm.speciality_id,
    ]
    form_ajax_refs = {
        "user": {
            "fields": ("id",),
            "order_by": "id",
        },
        "speciality": {
            "fields": ("id",),
            "order_by": "id",
        },
        "courses_requests": {
            "fields": ("student_id",),
            "order_by": "student_id",
        },
        "comments": {
            "fields": ("student_id",),
            "order_by": "student_id",
        },
    }
    form_columns = [
        StudentsOrm.user_id,
        StudentsOrm.class_id,
        StudentsOrm.university_id,
        StudentsOrm.speciality_id,
        StudentsOrm.is_freshman,
    ]
    column_default_sort = [("university_id", True)]
