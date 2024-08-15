from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from common.unit_of_work import IUnitOfWork, UnitOfWork
from respository.storage import Storage, YandexStorage
from schemas import UserRead
from schemas.lecturer import LecturerInDB
from schemas.oauth_password import OAuth2PasswordSpecialForm
from schemas.pagination import Pagination
from schemas.student import StudentInDBWithSpeciality
from services import AuthService
from services.lecturer import LecturerService
from services.student import StudentService
from storage import AsyncSessionFactory

get_current_student = StudentService().get_current_student
get_current_lecturer = LecturerService().get_current_lecturer
CurrentStudentDep = Annotated[
    StudentInDBWithSpeciality, Depends(dependency=get_current_student)
]
CurrentLecturerDep = Annotated[LecturerInDB, Depends(dependency=get_current_lecturer)]
get_current_active_user = AuthService(is_active=True).get_current_user
get_current_verified_user = AuthService(
    is_verified=True, is_active=True
).get_current_user
get_current_superuser = AuthService(is_superuser=True, is_active=True).get_current_user
get_current_verified_superuser = AuthService(
    is_superuser=True,
    is_active=True,
    is_verified=True,
).get_current_user
UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
CurrentActiveUserDep = Annotated[UserRead, Depends(get_current_active_user)]
CurrentVerifiedUserDep = Annotated[UserRead, Depends(get_current_verified_user)]
CurrentSuperUserDep = Annotated[UserRead, Depends(get_current_superuser)]
CurrentVerifiedSuperUserDep = Annotated[
    UserRead, Depends(get_current_verified_superuser)
]
SessionDep = Annotated[AsyncSession, Depends(AsyncSessionFactory().get_async_session)]
OAuth2SpecialDep = Annotated[OAuth2PasswordSpecialForm, Depends()]
OAuth2Dep = Annotated[OAuth2PasswordRequestForm, Depends()]
PaginationDep = Annotated[Pagination, Depends()]
StorageDep = Annotated[Storage, Depends(YandexStorage)]