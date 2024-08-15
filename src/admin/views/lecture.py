from models.lecture import LecturesOrm
from .base import BaseModelView, get_datetime


class LectureAdmin(BaseModelView, model=LecturesOrm):
    name = "Lecture"
    name_plural = "Lectures"
    icon = "fas fa-file-signature"
    pk_columns = [LecturesOrm.id]
    form_ajax_refs = {
        "lecturer_course": {
            "fields": ("id",),
            "order_by": "id",
        },
        "file": {
            "fields": ("id",),
            "order_by": "id",
        },
    }
    column_formatters = get_datetime(LecturesOrm)
    column_formatters[LecturesOrm.body] = lambda m, a: (
        m.body if len(m.body) < 15 else m.body[:15]
    )
    column_formatters_detail = get_datetime(LecturesOrm)
    column_formatters_detail[LecturesOrm.body] = lambda m, a: (
        m.body if len(m.body) < 15 else m.body[:15]
    )

    column_list = [
        LecturesOrm.title,
        LecturesOrm.body,
        LecturesOrm.file,
        LecturesOrm.lecturer_course,
        LecturesOrm.added_at,
        LecturesOrm.updated_at,
    ]
    form_columns = [
        LecturesOrm.lecturer_course_id,
        LecturesOrm.file_id,
        LecturesOrm.title,
        LecturesOrm.body,
    ]
