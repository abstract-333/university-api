import secrets
from typing import Any
import uuid
from argon2._password_hasher import PasswordHasher
from mypy.nodes import EXCLUDED_PROTOCOL_ATTRIBUTES
from pydantic import EmailStr
from common import IUnitOfWork
from exception import (
    ExceptionForbidden403,
    ExceptionNotFound404,
    ExceptionBadRequest400,
    ExceptionNotAcceptable406,
)
from exception.error_code import ErrorCode
from schemas import (
    UserRead,
    UserUpdate,
)
from specification.user import UserEmailSpecification, UserIdSpecification


class UserService:
    def __init__(
        self,
    ) -> None:
        self.password_hasher = PasswordHasher(
            hash_len=32, salt_len=16, memory_cost=65536 // 2
        )

    @classmethod
    async def get_user_by_email(
        cls,
        uow: IUnitOfWork,
        email: EmailStr,
    ) -> UserRead | None:
        async with uow:
            user: UserRead | None = await uow.user.get_user(
                specification=UserEmailSpecification(email=email)
            )
            return user

    @classmethod
    async def get_user_by_id(
        cls,
        uow: IUnitOfWork,
        user_id: uuid.UUID,
    ) -> UserRead | None:
        async with uow:
            user: UserRead | None = await uow.user.get_user(
                specification=UserIdSpecification(id=user_id)
            )
            return user

    @classmethod
    async def edit_user(
        cls,
        uow: IUnitOfWork,
        user_data: dict,
        user_id: uuid.UUID,
    ) -> None:
        async with uow:
            await uow.user.edit_user(
                user_data=user_data, specification=UserIdSpecification(id=user_id)
            )
            await uow.commit()

    async def hash_password(self, password: str) -> str:
        return self.password_hasher.hash(password=password)

    async def update_user(
        self,
        updated_user: UserUpdate,
        old_user: UserRead,
        uow: IUnitOfWork,
    ) -> UserRead | None:
        if updated_user == old_user:
            return old_user

        user_id: uuid.UUID = old_user.id
        user_from_db: UserRead | None = await self.get_user_by_id(
            uow=uow, user_id=user_id
        )

        if user_from_db is None:
            raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)

        if updated_user.email and updated_user.email != old_user.email:
            user_same_email: UserRead | None = await self.get_user_by_email(
                uow=uow,
                email=updated_user.email,
            )

            if user_same_email is not None:
                raise ExceptionNotAcceptable406(detail=ErrorCode.EMAIL_ALREADY_EXISTS)

        updated_user_dict: dict[str, Any] = updated_user.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude_defaults=True,
            exclude=[
                "password",
            ],
        )
        if updated_user.password is not None:
            updated_user_dict["hashed_password"] = await self.hash_password(
                password=updated_user.password
            )

        await self.edit_user(uow=uow, user_data=updated_user_dict, user_id=user_id)
        returned_user: UserRead | None = await self.get_user_by_id(
            user_id=user_id, uow=uow
        )

        if not returned_user:
            raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)

        return returned_user

    async def deactivate_user(
        self,
        user_id: str,
        uow: IUnitOfWork,
    ) -> None:
        user_from_db: UserRead | None = await self.get_user_by_id(
            uow=uow, user_id=uuid.UUID(user_id)
        )

        # Ensures that user is existed, and raise exception otherwise
        if user_from_db is not None:
            raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)

        await self.edit_user(
            uow=uow,
            user_data={"is_active": False},
            user_id=uuid.UUID(user_id),
        )

    async def check_credentials_to_verify(self, user_data: UserRead) -> UserRead:
        """Checks that user is active and verified, in order to verify the email,
        otherwise it will raise exception"""
        if not user_data.is_active:
            raise ExceptionForbidden403(detail=ErrorCode.USER_INACTIVE)

        if user_data.is_verified:
            raise ExceptionForbidden403(detail=ErrorCode.USER_ALREADY_VERIFIED)

        return user_data

    async def verify_account(
        self,
        user: UserRead,
        uow: IUnitOfWork,
    ) -> str:
        user_from_db: UserRead | None = await self.get_user_by_id(
            user_id=user.id,
            uow=uow,
        )
        if user_from_db is None:
            raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)

        if user_from_db.is_verified:
            raise ExceptionBadRequest400(detail=ErrorCode.USER_ALREADY_VERIFIED)

        user_updating: UserRead = user_from_db
        user_updating.is_verified = True
        await self.edit_user(
            user_data=user_updating.model_dump(),
            user_id=user_updating.id,
            uow=uow,
        )
        return f"""<div dir="rtl"><center>
                                 <h1>تم توثيق البريد الالكتروني بنجاح</h1>
                                 <h2>شكراً لك {user.first_name} {user.last_name}</h2>
                                 </center>
                                 </div>"""

    async def recover_password(
        self,
        email: EmailStr,
        uow: IUnitOfWork,
    ) -> str:
        try:
            user_from_db: UserRead | None = await self.get_user_by_email(
                uow=uow,
                email=email,
            )
            if user_from_db is None:
                raise ExceptionNotFound404(detail=ErrorCode.USER_NOT_EXISTS)
            password = secrets.token_urlsafe(20)
            hashed_random_password = await self.hash_password(password=password)
            await self.edit_user(
                user_id=user_from_db.id,
                user_data={"hashed_password": hashed_random_password},
                uow=uow,
            )
            print(password)
            return password

        except Exception as exception:
            raise exception
