from abc import abstractmethod, ABC
from typing import Any, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import (
    ColumnExpressionArgument,
    Delete,
    Insert,
    Result,
    ScalarResult,
    Select,
    Update,
    insert,
    select,
    update,
    delete,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from models import BaseModelORM
from sqlalchemy.orm import InstrumentedAttribute

Schema = TypeVar("Schema", bound=BaseModel)

ColumnExpressionOrAnyArgument = (
    Any | ColumnExpressionArgument
)  # Type for options parameter


class AbstractSQLRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> None:
        ...

    @abstractmethod
    async def edit_one(
        self,
        data: dict,
        arguments: ColumnExpressionOrAnyArgument,
    ) -> None:
        ...

    @abstractmethod
    async def find_by(
        self,
        *options: Any,
        offset: int,
        limit: int,
        join_conditions: tuple[Any] = tuple(),
        schema: Type[Schema],
        arguments: ColumnExpressionOrAnyArgument,
    ) -> list[Schema] | None:
        ...

    @abstractmethod
    async def find_one(
        self,
        *options: Any,
        join_conditions: tuple[Any] = tuple(),
        schema: Type[Schema],
        arguments: ColumnExpressionOrAnyArgument,
    ) -> Schema | None:
        ...

    @abstractmethod
    async def delete_one(
        self,
        arguments: ColumnExpressionOrAnyArgument,
    ) -> None:
        ...


class SQLAlchemyRepository(AbstractSQLRepository, ABC):
    model_cls: type[BaseModelORM | Any]

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def add_one(self, data: dict) -> None:
        stmt: Insert = insert(table=self.model_cls).values(**data)
        await self.session.execute(statement=stmt)

    async def edit_one(
        self,
        data: dict,
        arguments: ColumnExpressionOrAnyArgument = True,
    ) -> None:
        stmt: Update = update(table=self.model_cls)

        stmt = stmt.where(arguments).values(**data)

        await self.session.execute(statement=stmt)

    async def find_by(
        self,
        *options: ExecutableOption,
        offset: int,
        limit: int,
        join_conditions: tuple[InstrumentedAttribute[BaseModelORM]] = tuple(),
        schema: Type[Schema],
        arguments: ColumnExpressionOrAnyArgument = True,
    ) -> list[Schema] | None:
        query: Select[tuple[BaseModelORM]] = select(self.model_cls)

        for join_condition in join_conditions:
            query = query.join(join_condition)

        if options:
            query = query.options(*options)

        query = query.filter(arguments).offset(offset=offset).limit(limit=limit)

        query_result: Result[tuple[BaseModelORM]] = await self.session.execute(
            statement=query
        )
        scalar_result: ScalarResult[BaseModelORM] = query_result.scalars()

        if not scalar_result:
            return None
        result: list[Schema] = [
            element.to_read_model(schema=schema) for element in scalar_result.all()
        ]

        if not result:
            return None

        return result

    async def find_one(
        self,
        *options: ExecutableOption,
        join_conditions: tuple[InstrumentedAttribute[BaseModelORM]] = tuple(),
        schema: Type[Schema],
        arguments: ColumnExpressionOrAnyArgument = True,
    ) -> Schema | None:
        query: Select[tuple[BaseModelORM]] = select(self.model_cls)

        for join_condition in join_conditions:
            query = query.join(join_condition)

        if options:
            query = query.options(*options)

        query = query.filter(arguments).limit(limit=1)

        query_result: Result[tuple[BaseModelORM]] = await self.session.execute(
            statement=query
        )
        result: BaseModelORM | None = query_result.scalar_one_or_none()

        return result if result is None else result.to_read_model(schema=schema)

    async def delete_one(
        self,
        arguments: ColumnExpressionOrAnyArgument = True,
    ) -> None:
        stmt: Delete = delete(table=self.model_cls)

        stmt = stmt.where(arguments)
        await self.session.execute(statement=stmt)
