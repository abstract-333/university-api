import datetime
from models.active_session import ActiveSessionsOrm
from .base import BaseModelView


class ActiveSessionAdmin(BaseModelView, model=ActiveSessionsOrm):
    name = "Active Session"
    name_plural = "Active Sessions"
    icon = "fas fa-undo"
    pk_columns = [ActiveSessionsOrm.id]
    form_ajax_refs = {
        "user": {
            "fields": ("id",),
            "order_by": "id",
        },
    }
    column_formatters = {
        ActiveSessionsOrm.added_at: lambda m, a: datetime.datetime.fromtimestamp(
            m.added_at
        ),
        ActiveSessionsOrm.expire_at: lambda m, a: datetime.datetime.fromtimestamp(
            m.expire_at
        ),
    }
    column_formatters_detail = {
        ActiveSessionsOrm.added_at: lambda m, a: datetime.datetime.fromtimestamp(
            m.added_at
        ),
        ActiveSessionsOrm.expire_at: lambda m, a: datetime.datetime.fromtimestamp(
            m.expire_at
        ),
    }

    column_list = [
        ActiveSessionsOrm.user,
        ActiveSessionsOrm.device_name,
        ActiveSessionsOrm.device_id,
        ActiveSessionsOrm.added_at,
        ActiveSessionsOrm.expire_at,
    ]

    form_columns = [
        ActiveSessionsOrm.user_id,
        ActiveSessionsOrm.device_name,
        ActiveSessionsOrm.device_id,
        ActiveSessionsOrm.refresh_token,
        ActiveSessionsOrm.expire_at,
    ]
