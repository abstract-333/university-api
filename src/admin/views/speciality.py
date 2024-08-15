from models import SpecialitiesOrm
from .base import BaseModelView


class SpecialityAdmin(BaseModelView, model=SpecialitiesOrm):
    name = "Speciality"
    name_plural = "Specialities"
    icon = "fa-solid fa-palette"
    pk_columns = [SpecialitiesOrm.name]
    form_ajax_refs = {
        "faculty": {
            "fields": ("name",),
            "order_by": "name",
        },
        "students": {
            "fields": ("speciality_id",),
            "order_by": "speciality_id",
        },
        "speciality_courses": {
            "fields": ("speciality_id",),
            "order_by": "speciality_id",
        },
    }
    column_list = [
        SpecialitiesOrm.name,
        SpecialitiesOrm.faculty_name,
        SpecialitiesOrm.speciality_courses,
    ]
    form_excluded_columns = [
        SpecialitiesOrm.faculty,
        SpecialitiesOrm.students,
        SpecialitiesOrm.id,
    ]
    column_details_list = [
        SpecialitiesOrm.id,
        SpecialitiesOrm.name,
        SpecialitiesOrm.faculty,
    ]
    column_searchable_list = [SpecialitiesOrm.name]
    column_default_sort = [("name", True)]
