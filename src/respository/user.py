from abc import ABC, abstractmethod

from models import UsersOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas import UserReadWithPassword
from specification.base import Specification
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def get_user(
        self,
        specification: Specification,
    ) -> UserReadWithPassword | None:
        ...

    @abstractmethod
    async def add_user(self, user_data: dict) -> None:
        ...

    @abstractmethod
    async def edit_user(
        self,
        user_data: dict,
        specification: Specification,
    ) -> None:
        ...


class UserRepository(SQLAlchemyRepository, UserRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[UsersOrm] = UsersOrm
        super().__init__(session=session)

    async def get_user(
        self,
        specification: Specification,
    ) -> UserReadWithPassword | None:
        user: UserReadWithPassword | None = await self.find_one(
            schema=UserReadWithPassword,
            arguments=specification.is_satisfied_by(),
        )
        return user

    async def add_user(self, user_data: dict) -> None:
        """Add user to db"""
        await self.add_one(data=user_data)

    async def edit_user(
        self,
        user_data: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(
            data=user_data,
            arguments=specification.is_satisfied_by(),
        )
