from sqladmin import ModelView
from starlette.requests import Request

from storage import AsyncSessionFactory

import datetime

from models.base import BaseModelORM


class BaseModelView(ModelView):
    session_maker = AsyncSessionFactory().get_async_session_maker()
    is_async = True
    can_edit = True
    can_delete = True
    form_include_pk = True
    can_create = True
    can_export = True
    can_view_details = True
    page_size = 20
    save_as = True
    save_as_continue = True

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


def get_datetime(orm_model: type[BaseModelORM]) -> dict:
    return {
        orm_model.added_at: lambda m, a: datetime.datetime.fromtimestamp(m.added_at),
        orm_model.updated_at: lambda m, a: datetime.datetime.fromtimestamp(
            m.updated_at
        ),
    }


def get_text_slice(orm_model: type[BaseModelORM], lenght: int = 15) -> dict:
    return {
        orm_model.body: lambda m, a: (
            m.body if len(m.body) < lenght else m.body[:lenght]
        ),
    }
