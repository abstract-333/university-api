from models.file import FilesOrm
from .base import BaseModelView, get_datetime


class FileAdmin(BaseModelView, model=FilesOrm):
    name = "File"
    name_plural = "Files"
    icon = "fa-solid fa-file"
    pk_columns = [FilesOrm.id]
    column_formatters = get_datetime(FilesOrm)
    column_formatters[FilesOrm.name] = lambda m, a: (
        m.name if len(m.name) < 15 else m.name[:15]
    )
    column_formatters_detail = get_datetime(FilesOrm)
    column_formatters_detail[FilesOrm.name] = lambda m, a: (
        m.name if len(m.name) < 15 else m.name[:15]
    )
    form_ajax_refs = {
        "lectures": {
            "fields": ("file_id",),
            "order_by": "file_id",
        },
    }
    column_list = [
        FilesOrm.name,
        FilesOrm.file_id,
        FilesOrm.size,
        FilesOrm.added_at,
        FilesOrm.updated_at,
    ]

    form_columns = [
        FilesOrm.name,
        FilesOrm.file_id,
        FilesOrm.size,
    ]
