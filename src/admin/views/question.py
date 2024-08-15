from models.question import QuestionsOrm
from .base import BaseModelView, get_datetime


class QuestionAdmin(BaseModelView, model=QuestionsOrm):
    name = "Question"
    name_plural = "Questions"
    icon = "fas fa-clipboard-question"
    pk_columns = [QuestionsOrm.id]
    form_ajax_refs = {
        "lecturer_course": {
            "fields": ("id",),
            "order_by": "id",
        },
    }
    column_formatters = get_datetime(QuestionsOrm)
    column_formatters[QuestionsOrm.body] = lambda m, a: (
        m.body if len(m.body) < 15 else m.body[:15]
    )
    column_formatters_detail = get_datetime(QuestionsOrm)
    column_formatters_detail[QuestionsOrm.body] = lambda m, a: (
        m.body if len(m.body) < 15 else m.body[:15]
    )

    column_list = [
        QuestionsOrm.body,
        QuestionsOrm.choices,
        QuestionsOrm.right_choice,
        QuestionsOrm.lecturer_course,
        QuestionsOrm.is_visible,
        QuestionsOrm.added_at,
        QuestionsOrm.updated_at,
    ]

    form_columns = [
        QuestionsOrm.lecturer_course_id,
        QuestionsOrm.body,
        QuestionsOrm.choices,
        QuestionsOrm.right_choice,
        QuestionsOrm.is_visible,
    ]
