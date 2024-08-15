from fastapi import APIRouter, BackgroundTasks
from pydantic.networks import EmailStr
from starlette import status
from starlette.responses import HTMLResponse

from api.docs import (
    get_user_response,
    update_user_response,
    request_verify_response,
    verify_email_response,
    delete_user_response,
    register_user_responses,
)
from api.docs.user import reset_password_response
from dependencies.dependencies import (
    UOWDep,
    CurrentVerifiedUserDep,
    CurrentActiveUserDep,
)
from schemas import UserCreate
from schemas import UserRead, UserUpdate
from services import AuthService, EmailService, UserService

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    responses=register_user_responses,
)
async def register_user(
    user_data: UserCreate,
    uow: UOWDep,
):
    auth_service = AuthService()
    if await auth_service.register_new_user(user_data=user_data, uow=uow):
        return {"message": "Account created!!!"}


@user_router.get(
    path="/me",
    responses=get_user_response,
)
async def get_user(
    current_user: CurrentActiveUserDep,
):
    return current_user


@user_router.patch(
    path="",
    responses=update_user_response,
)
async def patch_user(
    uow: UOWDep,
    current_user: CurrentActiveUserDep,
    updated_user: UserUpdate,
):
    user_service = UserService()
    old_user: UserRead = current_user
    return await user_service.update_user(
        uow=uow, updated_user=updated_user, old_user=old_user
    )


@user_router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=delete_user_response,
)
async def delete_user(
    uow: UOWDep,
    current_user: CurrentVerifiedUserDep,
):
    user_service = UserService()
    await user_service.deactivate_user(uow=uow, user_id=str(current_user.id))


@user_router.get(
    path="/request-verify",
    status_code=status.HTTP_202_ACCEPTED,
    responses=request_verify_response,
)
async def request_email_verify(
    current_user: CurrentActiveUserDep,
    background_tasks: BackgroundTasks,
) -> dict[str, str]:
    auth_service = AuthService()
    user_service = UserService()
    email_service = EmailService()
    user_data: UserRead = await user_service.check_credentials_to_verify(current_user)
    jwt_token: bytes = await auth_service._create_jwt_access_token(user=user_data)
    jwt_token_str: str = str(jwt_token, "utf-8")
    background_tasks.add_task(
        email_service.send_email,
        current_user.first_name + " " + current_user.last_name,
        email_service.EMAIL_CONFIRM,
        current_user.email,
        jwt_token_str,
    )

    return {"message": "Verification email sent successfully"}


@user_router.get(
    path="/verify-email",
    responses=verify_email_response,
)
async def verify_email(
    token: str,
    uow: UOWDep,
):
    auth_service = AuthService()
    user_service = UserService()
    user: UserRead = await auth_service.validate_access_token(token=token)
    html_content_response = await user_service.verify_account(user=user, uow=uow)
    return HTMLResponse(status_code=200, content=html_content_response)


@user_router.post(
    path="/forget-password",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=reset_password_response,
)
async def forget_password(
    email: EmailStr,
    uow: UOWDep,
    background_tasks: BackgroundTasks,
):
    user_service = UserService()
    email_service = EmailService()
    password = await user_service.recover_password(email=email, uow=uow)
    background_tasks.add_task(
        email_service.send_email_reset_password,
        email_service.RESET_PASSWORD,
        email,
        password,
    )

    return {"message": "Password reset message sent successfully"}
