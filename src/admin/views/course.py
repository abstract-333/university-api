from typing import Any
from models import CoursesOrm
from .base import BaseModelView


class CourseAdmin(BaseModelView, model=CoursesOrm):
    name = "Course"
    name_plural = "Courses"
    icon = "fa-solid fa-newspaper"
    pk_columns = [CoursesOrm.name]
    form_ajax_refs = {
        "speciality_courses": {
            "fields": ("course_name",),
            "order_by": "course_name",
        },
    }

    column_list = [CoursesOrm.name]
    column_searchable_list = [CoursesOrm.name]
    form_excluded_columns = [CoursesOrm.speciality_courses]
    column_default_sort: list[Any] = [("name", True)]
