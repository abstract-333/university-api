from models import UsersOrm
from .base import BaseModelView, get_datetime


class UserAdmin(BaseModelView, model=UsersOrm):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user-group"
    can_create = False
    pk_columns = [UsersOrm.id]

    form_ajax_refs = {
        "students": {
            "fields": ("user_id",),
            "order_by": "user_id",
        },
        "lecturers": {
            "fields": ("user_id",),
            "order_by": "user_id",
        },
        "lecturers_requests": {
            "fields": ("user_id",),
            "order_by": "user_id",
        },
        "courses_requests": {
            "fields": ("processed_by",),
            "order_by": "processed_by",
        },
        "active_sessions": {
            "fields": ("user_id",),
            "order_by": "user_id",
        },
    }

    column_list = [
        UsersOrm.full_name,
        UsersOrm.email,
        UsersOrm.added_at,
        UsersOrm.updated_at,
        UsersOrm.is_active,
        UsersOrm.is_verified,
        UsersOrm.is_superuser,
    ]
    column_formatters = get_datetime(UsersOrm)
    column_formatters_detail = get_datetime(UsersOrm)
    form_excluded_columns = [
        UsersOrm.students,
        UsersOrm.id,
        UsersOrm.updated_at,
        UsersOrm.added_at,
        UsersOrm.hashed_password,
        UsersOrm.lecturers,
        UsersOrm.active_sessions,
        UsersOrm.lecturers_requests,
    ]
    column_details_exclude_list = [UsersOrm.hashed_password]
    column_searchable_list = [UsersOrm.email, UsersOrm.first_name, UsersOrm.last_name]
    column_default_sort = [("id", True)]
