from models import CommentsOrm
from .base import BaseModelView, get_datetime


class CommentAdmin(BaseModelView, model=CommentsOrm):
    name = "Comment"
    name_plural = "Comments"
    icon = "fa-solid fa-comment"
    pk_columns = [CommentsOrm.id]
    form_ajax_refs = {
        "post": {
            "fields": ("id",),
            "order_by": "id",
        },
        "lecturer": {
            "fields": ("id",),
            "order_by": "id",
        },
        "student": {
            "fields": ("id",),
            "order_by": "id",
        },
    }
    column_formatters = get_datetime(CommentsOrm)
    column_formatters[CommentsOrm.body] = lambda m, a: (
        m.body if len(m.body) < 15 else m.body[:15]
    )
    column_formatters_detail = get_datetime(CommentsOrm)
    column_formatters_detail[CommentsOrm.body] = lambda m, a: (
        m.body if len(m.body) < 15 else m.body[:15]
    )

    column_list = [
        CommentsOrm.body,
        CommentsOrm.author_type,
        CommentsOrm.student,
        CommentsOrm.lecturer,
        CommentsOrm.added_at,
        CommentsOrm.updated_at,
    ]

    form_columns = [
        CommentsOrm.post_id,
        CommentsOrm.body,
        CommentsOrm.student_id,
        CommentsOrm.lecturer_id,
        CommentsOrm.author_type,
    ]
