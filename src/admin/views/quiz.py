import datetime
from models.quiz import QuizzesOrm
from .base import BaseModelView, get_datetime


class QuizAdmin(BaseModelView, model=QuizzesOrm):
    name = "Quiz"
    name_plural = "Quizzes"
    icon = "fas fa-clipboard-list"
    pk_columns = [QuizzesOrm.id]
    form_ajax_refs = {
        "lecturer_course": {
            "fields": ("id",),
            "order_by": "id",
        },
        "quizzes_results": {
            "fields": ("quiz_id",),
            "order_by": "quiz_id",
        },
    }
    column_formatters = get_datetime(QuizzesOrm)
    column_formatters[QuizzesOrm.title] = lambda m, a: (
        m.title if len(m.title) < 15 else m.title[:15]
    )
    column_formatters[
        QuizzesOrm.start_date
    ] = lambda m, a: datetime.datetime.fromtimestamp(m.start_date)
    column_formatters[
        QuizzesOrm.end_date
    ] = lambda m, a: datetime.datetime.fromtimestamp(m.end_date)
    column_formatters_detail = get_datetime(QuizzesOrm)
    column_formatters_detail[QuizzesOrm.title] = lambda m, a: (
        m.title if len(m.title) < 15 else m.title[:15]
    )
    column_formatters_detail[
        QuizzesOrm.start_date
    ] = lambda m, a: datetime.datetime.fromtimestamp(m.start_date)
    column_formatters_detail[
        QuizzesOrm.end_date
    ] = lambda m, a: datetime.datetime.fromtimestamp(m.end_date)

    column_list = [
        QuizzesOrm.title,
        QuizzesOrm.duration,
        QuizzesOrm.number_of_questions,
        QuizzesOrm.mark,
        QuizzesOrm.start_date,
        QuizzesOrm.end_date,
        QuizzesOrm.added_at,
        QuizzesOrm.updated_at,
    ]

    form_columns = [
        QuizzesOrm.title,
        QuizzesOrm.lecturer_course_id,
        QuizzesOrm.duration,
        QuizzesOrm.number_of_questions,
        QuizzesOrm.mark,
        QuizzesOrm.start_date,
        QuizzesOrm.end_date,
    ]
