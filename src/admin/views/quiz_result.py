from models.quiz_result import QuizzesResultsOrm
from .base import BaseModelView, get_datetime


class QuizResultAdmin(BaseModelView, model=QuizzesResultsOrm):
    name = "Quiz Result"
    name_plural = "Quizzes Results"
    icon = "fas fa-spell-check"
    pk_columns = [QuizzesResultsOrm.id]
    form_ajax_refs = {
        "quiz": {
            "fields": ("id",),
            "order_by": "id",
        },
        "enrolled_course": {
            "fields": ("id",),
            "order_by": "id",
        },
    }
    column_formatters = get_datetime(QuizzesResultsOrm)
    column_formatters_detail = get_datetime(QuizzesResultsOrm)

    column_list = [
        QuizzesResultsOrm.quiz,
        QuizzesResultsOrm.enrolled_course,
        QuizzesResultsOrm.result,
        QuizzesResultsOrm.added_at,
        QuizzesResultsOrm.updated_at,
    ]

    form_columns = [
        QuizzesResultsOrm.enrolled_course_id,
        QuizzesResultsOrm.quiz_id,
        QuizzesResultsOrm.result,
    ]
