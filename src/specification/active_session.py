import uuid
from abc import ABC

from sqlalchemy import ColumnElement

from models.active_session import ActiveSessionsOrm
from specification.base import SpecificationSQLAlchemy


class ActiveSessionsBaseSpecification(SpecificationSQLAlchemy, ABC):
    def __init__(self) -> None:
        self.model = ActiveSessionsOrm


class SessionUserIdSpecification(ActiveSessionsBaseSpecification):
    def __init__(self, user_id: uuid.UUID) -> None:
        super().__init__()
        self.user_id: uuid.UUID = user_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.user_id == self.user_id


class SessionDeviceIdSpecification(ActiveSessionsBaseSpecification):
    def __init__(self, device_id: str) -> None:
        super().__init__()
        self.device_id: str = device_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.device_id == self.device_id


class SessionRefreshTokenSpecification(ActiveSessionsBaseSpecification):
    def __init__(self, refresh_token: str) -> None:
        super().__init__()
        self.refresh_token: str = refresh_token

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.refresh_token == self.refresh_token


class SessionIdSpecification(ActiveSessionsBaseSpecification):
    def __init__(self, session_id: uuid.UUID) -> None:
        super().__init__()
        self.session_id: uuid.UUID = session_id

    def is_satisfied_by(self) -> ColumnElement[bool]:
        return self.model.id == self.session_id
