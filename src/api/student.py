import uuid
from fastapi import APIRouter
from starlette import status

from api.docs import (
    register_student_response,
    update_student_response,
    get_student_response,
    get_tokens_student_response,
    get_me_student_response,
    update_student_state_response,
)
from dependencies.dependencies import (
    CurrentStudentDep,
    PaginationDep,
    UOWDep,
    CurrentVerifiedUserDep,
)
from schemas import StudentCreate, StudentUpdate
from schemas.auth import AccessRefreshTokens
from schemas.student import StudentCreateFull, StudentUpdateState
from services import StudentService
from services.auth import AuthService

student_router = APIRouter(
    prefix="/student",
    tags=["Student"],
)


@student_router.post(
    path="/get-tokens",
    status_code=status.HTTP_200_OK,
    responses=get_tokens_student_response,
)
async def get_access_refresh_tokens_student(
    uow: UOWDep,
    refresh_token: str,
    student_id: uuid.UUID,
    device_id: str,
    current_user: CurrentVerifiedUserDep,
):
    student_service = StudentService()
    auth_service = AuthService()

    new_refresh_token: bytes = await auth_service.create_refresh_token(
        refresh_token=refresh_token,
        device_id=device_id,
        uow=uow,
    )
    access_token: bytes = await student_service.make_token_student(
        student_id=student_id,
        uow=uow,
    )
    return AccessRefreshTokens(
        access_token=access_token,
        refresh_token=new_refresh_token,
    )


@student_router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    responses=register_student_response,
)
async def register_student(
    uow: UOWDep,
    student_data: StudentCreate,
    current_user: CurrentVerifiedUserDep,
):
    student_service = StudentService()
    student_data_full = StudentCreateFull(
        university_id=student_data.university_id,
        user_id=current_user.id,
        class_id=student_data.class_id,
        is_freshman=student_data.is_freshman,
        speciality_id=student_data.speciality_id,
    )
    await student_service.register_student(create_student=student_data_full, uow=uow)


@student_router.patch(
    path="",
    status_code=status.HTTP_200_OK,
    responses=update_student_response,
)
async def update_student(
    uow: UOWDep,
    student_data: StudentUpdate,
    current_student: CurrentStudentDep,
):
    student_service = StudentService()
    return await student_service.update_student(
        updated_student=student_data,
        student_id=current_student.id,
        uow=uow,
    )


@student_router.patch(
    path="/state",
    status_code=status.HTTP_200_OK,
    responses=update_student_state_response,
)
async def update_student_state(
    uow: UOWDep,
    student_data: StudentUpdateState,
    current_student: CurrentStudentDep,
):
    student_service = StudentService()
    return await student_service.update_student_state(
        updated_student=student_data,
        student_id=current_student.id,
        uow=uow,
    )


@student_router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    responses=get_me_student_response,
)
async def get_student(
    uow: UOWDep,
    current_student: CurrentStudentDep,
):
    return current_student


@student_router.get(
    path="/all",
    status_code=status.HTTP_200_OK,
    responses=get_student_response,
)
async def get_all_student_records(
    uow: UOWDep,
    current_user: CurrentVerifiedUserDep,
    pagination: PaginationDep,
):
    student_service = StudentService()
    return await student_service.get_students_by_user_id(
        user_id=current_user.id, uow=uow
    )
