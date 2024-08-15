from models import FacultiesOrm
from .base import BaseModelView


class FacultyAdmin(BaseModelView, model=FacultiesOrm):
    name = "Faculty"
    name_plural = "Faculties"
    icon = "fa-solid fa-building-columns"

    form_ajax_refs = {
        "specialities": {
            "fields": ("faculty_name",),
            "order_by": "faculty_name",
        },
        "lecturers": {
            "fields": ("faculty_name",),
            "order_by": "faculty_name",
        },
        "lecturers_requests": {
            "fields": ("faculty_name",),
            "order_by": "faculty_name",
        },
    }
    column_list = [
        FacultiesOrm.name,
        FacultiesOrm.max_class,
    ]
    form_columns = [FacultiesOrm.name, FacultiesOrm.max_class]
    column_searchable_list = [FacultiesOrm.name, FacultiesOrm.max_class]
