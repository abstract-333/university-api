from uuid import UUID


from fastapi import APIRouter, UploadFile
from starlette.responses import StreamingResponse
from dependencies.dependencies import (
    CurrentStudentDep,
    StorageDep,
    UOWDep,
)
from services.file import FileService
from api.docs.file_student import download_file_responses

file_student_router = APIRouter(
    prefix="/file/student",
    tags=["File: Student"],
)


class UploadFileExtended(UploadFile):
    filename: str
    size: int


@file_student_router.get(
    path="/{file_id}",
    responses=download_file_responses,
)
async def download_file(
    file_id: UUID,
    uow: UOWDep,
    current_student: CurrentStudentDep,
    storage: StorageDep,
) -> StreamingResponse:
    file_service = FileService()
    return await file_service.download_file(
        id=file_id,
        uow=uow,
        storage=storage,
    )
