from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from models.active_session import ActiveSessionsOrm
from respository import SQLAlchemyRepository, AbstractSQLRepository
from schemas.active_session import ActiveSessionInDB
from schemas.pagination import Pagination
from specification.base import Specification


class ActiveSessionRepositoryBase(AbstractSQLRepository, ABC):
    @abstractmethod
    async def add_session(self, session_data: dict) -> None:
        ...

    @abstractmethod
    async def get_sessions(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[ActiveSessionInDB] | None:
        ...

    @abstractmethod
    async def get_session(
        self,
        specification: Specification,
    ) -> ActiveSessionInDB | None:
        ...

    @abstractmethod
    async def edit_session(
        self, session_edit: dict, specification: Specification
    ) -> None:
        ...

    @abstractmethod
    async def delete_session(
        self,
        specification: Specification,
    ) -> None:
        ...


class ActiveSessionRepository(SQLAlchemyRepository, ActiveSessionRepositoryBase):
    def __init__(self, session: AsyncSession) -> None:
        self.model_cls: type[ActiveSessionsOrm] = ActiveSessionsOrm
        super().__init__(session=session)

    async def add_session(self, session_data: dict) -> None:
        await self.add_one(data=session_data)

    async def get_sessions(
        self,
        specification: Specification,
        pagination: Pagination = Pagination(),
    ) -> list[ActiveSessionInDB] | None:
        sessions: list[ActiveSessionInDB] | None = await self.find_by(
            arguments=specification.is_satisfied_by(),
            schema=ActiveSessionInDB,
            offset=pagination.offset,
            limit=pagination.limit,
        )
        return sessions

    async def get_session(
        self,
        specification: Specification,
    ) -> ActiveSessionInDB | None:
        session: ActiveSessionInDB | None = await self.find_one(
            schema=ActiveSessionInDB,
            arguments=specification.is_satisfied_by(),
        )
        return session

    async def edit_session(
        self,
        session_edit: dict,
        specification: Specification,
    ) -> None:
        await self.edit_one(
            data=session_edit,
            arguments=specification.is_satisfied_by(),
        )

    async def delete_session(self, specification: Specification) -> None:
        await self.delete_one(arguments=specification.is_satisfied_by())
