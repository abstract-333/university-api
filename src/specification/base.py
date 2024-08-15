from abc import ABC, abstractmethod
from typing import Any, Generator, Protocol

from sqlalchemy import ColumnElement


from models.base import BaseModelORM

"""Source = https://github.com/u8slvn/sutoppu"""


class Specification(Protocol):
    def is_satisfied_by(self) -> Any:
        ...

    def __and__(self, spec: "Specification") -> Any:
        ...

    def __or__(self, spec: "Specification") -> Any:
        ...

    def __invert__(self) -> Any:
        ...


class SpecificationSQLAlchemy(ABC):
    @abstractmethod
    def is_satisfied_by(self) -> ColumnElement[bool]:
        ...

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def __and__(self, spec: Specification) -> "_AndSpecification":
        return _AndSpecification(spec_a=self, spec_b=spec)

    def __or__(self, spec: Specification) -> "_OrSpecification":
        return _OrSpecification(spec_a=self, spec_b=spec)

    def __invert__(self) -> "_NotSpecification":
        return _NotSpecification(spec=self)

    def __repr__(self) -> str:
        return f"<{self.class_name}>"


class _AndOrSpecification(SpecificationSQLAlchemy):
    """Base class for 'And' and 'Or' specifications."""

    def __init__(self, spec_a: Specification, spec_b: Specification) -> None:
        super().__init__()
        self._specs: tuple[Specification, Specification] = (
            spec_a,
            spec_b,
        )

    def is_satisfied_by(self) -> ColumnElement[bool]:
        results: Generator[ColumnElement[bool], None, None] = (
            spec.is_satisfied_by() for spec in self._specs
        )
        return self._check(*results)

    @abstractmethod
    def _check(
        self, spec_a: ColumnElement[bool], spec_b: ColumnElement[bool]
    ) -> ColumnElement[bool]:
        ...


class _AndSpecification(_AndOrSpecification):
    def _check(
        self, spec_a: ColumnElement[bool], spec_b: ColumnElement[bool]
    ) -> ColumnElement[bool]:
        return spec_b & spec_a


class _OrSpecification(_AndOrSpecification):
    def _check(
        self, spec_a: ColumnElement[bool], spec_b: ColumnElement[bool]
    ) -> ColumnElement[bool]:
        return spec_b | spec_a


class _NotSpecification(SpecificationSQLAlchemy):
    def __init__(self, spec: SpecificationSQLAlchemy) -> None:
        super().__init__()
        self._spec: SpecificationSQLAlchemy = spec

    def is_satisfied_by(self) -> ColumnElement[bool]:
        result: ColumnElement[bool] = self._spec.is_satisfied_by()
        return result != True
