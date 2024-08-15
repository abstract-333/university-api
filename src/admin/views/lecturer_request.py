from models.lecturer_request import LecturersRequestsOrm
from .base import BaseModelView, get_datetime


class LecturerRequestAdmin(BaseModelView, model=LecturersRequestsOrm):
    name = "Lecturer Request"
    name_plural = "Lecturers Requests"
    icon = "fa-solid fa-arrows-down-to-people"
    pk_columns = [LecturersRequestsOrm.id]

    form_ajax_refs = {
        "user": {
            "fields": ("id",),
            "order_by": "id",
        },
        "faculty": {
            "fields": ("name",),
            "order_by": "name",
        },
    }

    column_formatters = get_datetime(LecturersRequestsOrm)
    column_formatters[LecturersRequestsOrm.description] = lambda m, a: (
        m.description if len(m.description) < 15 else m.description[:15]
    )
    column_formatters_detail = get_datetime(LecturersRequestsOrm)
    column_formatters_detail[LecturersRequestsOrm.description] = lambda m, a: (
        m.description if len(m.description) < 15 else m.description[:15]
    )
    column_list = [
        LecturersRequestsOrm.user,
        LecturersRequestsOrm.faculty_name,
        LecturersRequestsOrm.description,
        LecturersRequestsOrm.is_accepted,
        LecturersRequestsOrm.processed_at,
        LecturersRequestsOrm.added_at,
        LecturersRequestsOrm.updated_at,
    ]
    column_searchable_list = [
        LecturersRequestsOrm.user_id,
        LecturersRequestsOrm.faculty_name,
        LecturersRequestsOrm.description,
    ]
    column_details_list = [
        LecturersRequestsOrm.id,
        LecturersRequestsOrm.faculty,
        LecturersRequestsOrm.user,
        LecturersRequestsOrm.user_id,
        LecturersRequestsOrm.faculty_name,
        LecturersRequestsOrm.description,
        LecturersRequestsOrm.is_accepted,
        LecturersRequestsOrm.processed_at,
    ]
    form_columns = [
        LecturersRequestsOrm.user_id,
        LecturersRequestsOrm.faculty_name,
        LecturersRequestsOrm.description,
        LecturersRequestsOrm.processed_at,
        LecturersRequestsOrm.is_accepted,
    ]
