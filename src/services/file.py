from typing import BinaryIO
from uuid import UUID

import nanoid
from starlette.responses import StreamingResponse

from common.unit_of_work import IUnitOfWork
from dependencies.dependencies import StorageDep
from exception.base import ExceptionNotFound404
from exception.error_code import ErrorCode
from schemas.file import FileCreate, FileInDB
from settings import settings_obj
from specification.file import FileFileIdSpecification, FileIdSpecification


class FileService:
    @classmethod
    async def _get_file_by_file_id(
        cls,
        file_id: str,
        uow: IUnitOfWork,
    ) -> FileInDB | None:
        async with uow:
            return await uow.file.get_file(
                specification=FileFileIdSpecification(file_id=file_id)
            )

    @classmethod
    async def _get_file_by_id(
        cls,
        id: UUID,
        uow: IUnitOfWork,
    ) -> FileInDB | None:
        async with uow:
            return await uow.file.get_file(specification=FileIdSpecification(id=id))

    @classmethod
    async def _add_file(
        cls,
        file_data: dict,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.file.add_file(file_data=file_data)
            await uow.commit()

    @classmethod
    async def _delete_file(
        cls,
        file_id: UUID,
        uow: IUnitOfWork,
    ) -> None:
        async with uow:
            await uow.file.delete_file(specification=FileIdSpecification(id=file_id))
            await uow.commit()

    async def upload_file(
        self,
        file_data: BinaryIO,
        file_name: str,
        file_size: int,
        uow: IUnitOfWork,
        storage: StorageDep,
    ) -> UUID:
        """uplaod file

        Args:
            file_data (BinaryIO):
            file_name (str):
            file_size (int):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: FILE_NOT_FOUND

            exception:

        Returns:
            UUID:
        """
        try:
            random_unique_name: str = nanoid.generate(size=settings_obj.SIZE)
            await storage.upload_file(file=file_data, filename=random_unique_name)
            file_create: FileCreate = FileCreate(
                file_id=random_unique_name, name=file_name, size=file_size
            )
            await self._add_file(file_data=file_create.model_dump(), uow=uow)

            file: FileInDB | None = await self._get_file_by_file_id(
                file_id=random_unique_name,
                uow=uow,
            )
            if file is None:
                raise ExceptionNotFound404(detail=ErrorCode.FILE_NOT_FOUND)

            return file.id

        except Exception as exception:
            raise exception

    async def download_file(
        self,
        id: UUID,
        uow: IUnitOfWork,
        storage: StorageDep,
    ) -> StreamingResponse:
        """download file

        Args:
            id (UUID):
            uow (IUnitOfWork):

        Raises:
            ExceptionNotFound404: FILE_NOT_FOUND
            exception:

        Returns:
            StreamingResponse
        """
        try:
            file: FileInDB | None = await self._get_file_by_id(id=id, uow=uow)
            if file is None:
                raise ExceptionNotFound404(detail=ErrorCode.FILE_NOT_FOUND)

            return await storage.download_file(
                file_id=file.file_id,
                file_name=file.name,
            )

        except Exception as exception:
            raise exception
