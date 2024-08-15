from models.speciality_course import SpecialityCoursesOrm
from .base import BaseModelView


class SpecialityCourseAdmin(BaseModelView, model=SpecialityCoursesOrm):
    name = "Speciality Course"
    name_plural = "Specialities Courses"
    icon = "fas fa-audio-description"
    pk_columns = [SpecialityCoursesOrm.id]
    form_ajax_refs = {
        "course": {
            "fields": ("name",),
            "order_by": "name",
        },
        "taught_courses": {
            "fields": ("speciality_course_id",),
            "order_by": "speciality_course_id",
        },
        "speciality": {
            "fields": ("id",),
            "order_by": "id",
        },
    }
    column_list = [
        SpecialityCoursesOrm.course_name,
        SpecialityCoursesOrm.speciality,
        SpecialityCoursesOrm.taught_courses,
        SpecialityCoursesOrm.course,
        SpecialityCoursesOrm.current_class,
        SpecialityCoursesOrm.semester,
    ]
    form_columns = [
        SpecialityCoursesOrm.course_name,
        SpecialityCoursesOrm.speciality_id,
        SpecialityCoursesOrm.current_class,
        SpecialityCoursesOrm.semester,
        SpecialityCoursesOrm.speciality_id,
    ]
    column_searchable_list = [
        SpecialityCoursesOrm.speciality,
        SpecialityCoursesOrm.course_name,
    ]
    column_default_sort = [("course_name", True)]
