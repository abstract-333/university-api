from uuid import UUID


from fastapi import APIRouter, UploadFile
from starlette.responses import StreamingResponse
from dependencies.dependencies import CurrentLecturerDep, StorageDep, UOWDep
from services.file import FileService
from starlette import status
from api.docs.file_leturer import download_file_responses, upload_file_responses

file_lecturer_router = APIRouter(
    prefix="/file/lecturer",
    tags=["File: Lecturer"],
)


class UploadFileExtended(UploadFile):
    filename: str
    size: int


@file_lecturer_router.post(
    path="",
    status_code=status.HTTP_200_OK,
    responses=upload_file_responses,
)
async def upload_file(
    file: UploadFileExtended,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    storage: StorageDep,
):
    file_service = FileService()

    return await file_service.upload_file(
        file_data=file.file,
        file_size=file.size,
        file_name=file.filename,
        uow=uow,
        storage=storage,
    )


@file_lecturer_router.get(
    path="/{file_id}",
    responses=download_file_responses,
)
async def download_file(
    file_id: UUID,
    uow: UOWDep,
    current_lecturer: CurrentLecturerDep,
    storage: StorageDep,
) -> StreamingResponse:
    file_service = FileService()
    return await file_service.download_file(
        id=file_id,
        uow=uow,
        storage=storage,
    )
