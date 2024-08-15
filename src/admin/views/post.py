from models.post import PostsOrm
from .base import BaseModelView, get_datetime


class PostAdmin(BaseModelView, model=PostsOrm):
    name = "Post"
    name_plural = "Posts"
    icon = "fas fa-edit"
    pk_columns = [PostsOrm.id]
    form_ajax_refs = {
        "lecturer_course": {
            "fields": ("id",),
            "order_by": "id",
        },
        "comments": {
            "fields": ("post_id",),
            "order_by": "post_id",
        },
    }
    column_formatters = get_datetime(PostsOrm)
    column_formatters[PostsOrm.body] = lambda m, a: (
        m.body if len(m.body) < 15 else m.body[:15]
    )
    column_formatters_detail = get_datetime(PostsOrm)
    column_formatters_detail[PostsOrm.body] = lambda m, a: (
        m.body if len(m.body) < 15 else m.body[:15]
    )
    column_list = [
        PostsOrm.body,
        PostsOrm.comments,
        PostsOrm.lecturer_course,
        PostsOrm.added_at,
        PostsOrm.updated_at,
    ]

    form_columns = [
        PostsOrm.lecturer_course_id,
        PostsOrm.body,
    ]
