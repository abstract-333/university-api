from fastapi import APIRouter
from starlette import status

from dependencies import UOWDep
from dependencies.dependencies import OAuth2SpecialDep
from services import AuthService
from .docs.auth import sign_in_response, sign_out_response, get_tokens_response

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth_router.post(
    path="/sign-in",
    status_code=status.HTTP_200_OK,
    responses=sign_in_response,
)
async def sign_in(
    uow: UOWDep,
    form_data: OAuth2SpecialDep,
):
    auth_service = AuthService(is_active=True)
    if form_data.device_id is None and form_data.device_name is None:
        auth_service.is_superuser = True
        auth_service.is_verified = True
        return await auth_service.authenticate_user(
            email=form_data.username,
            password=form_data.password,
            uow=uow,
        )
    return await auth_service.authenticate_user_using_device_id(
        email=form_data.username,
        password=form_data.password,
        device_id=form_data.device_id,
        device_name=form_data.device_name,
        uow=uow,
    )


@auth_router.post(
    path="/get-tokens",
    status_code=status.HTTP_200_OK,
    responses=get_tokens_response,
)
async def get_access_refresh_tokens(
    uow: UOWDep,
    refresh_token: str,
    device_id: str,
):
    auth_service = AuthService(is_active=True, is_verified=False)
    return await auth_service.create_tokens(
        refresh_token=refresh_token,
        device_id=device_id,
        uow=uow,
    )


@auth_router.post(
    path="/sign-out",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=sign_out_response,
)
async def sign_out(
    uow: UOWDep,
    refresh_token: str,
) -> None:
    auth_service = AuthService(is_active=True, is_verified=False)
    await auth_service.revoke_token(refresh_token=refresh_token, uow=uow)
