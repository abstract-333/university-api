from abc import ABC, abstractmethod
import io
from typing import BinaryIO

from fastapi.responses import StreamingResponse
import yadisk

from exception.base import ExceptionInternalServerError500
from settings import settings_obj

client = yadisk.AsyncClient(token=settings_obj.YANDEX_API, session="httpx")


class Storage(ABC):
    @abstractmethod
    async def download_file(
        self,
        file_id: str,
        file_name: str,
    ) -> StreamingResponse:
        ...

    @abstractmethod
    async def upload_file(
        self,
        file: BinaryIO,
        filename: str,
    ) -> None:
        ...

    @abstractmethod
    async def delete_file(
        self,
        file_name: str,
    ) -> None:
        ...


class YandexStorage(Storage):
    async def download_file(
        self,
        file_id: str,
        file_name: str,
    ) -> StreamingResponse:
        try:
            file = io.BytesIO()
            await client.download(f"/{file_id}", file)
            file.seek(0)
            return StreamingResponse(
                content=file,
                media_type="application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename={file_name}"},
            )

        except Exception as e:
            raise ExceptionInternalServerError500(detail=str(e))

    async def upload_file(self, file: BinaryIO, filename: str) -> None:
        try:
            contents: bytes = file.read()
            temp_file: io.BytesIO = io.BytesIO()
            temp_file.name = filename
            temp_file.write(contents)
            temp_file.seek(0)

            await client.upload(temp_file, f"/{filename}")

        except Exception as e:
            raise IOError(str(e))

    async def delete_file(
        self,
        file_name: str,
    ) -> None:
        await client.remove(f"/{file_name}", permanently=True)
