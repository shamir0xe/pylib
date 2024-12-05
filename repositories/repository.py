import logging
from dataclasses import dataclass
from typing import Generic, List, Optional, Tuple, Type, TypeVar
from sqlalchemy.orm import Session
from ..database.decorated_base import DecoratedBase
from ..decorators.db_session import db_session
from ..types.database_types import DatabaseTypes
from ..types.exception_types import ExceptionTypes
from .base_repository import BaseRepository

LOGGER = logging.getLogger(__name__)
T = TypeVar("T", bound=DecoratedBase)


@dataclass
class Repository(Generic[T], BaseRepository[T, str]):
    model: Type[T]

    @db_session(DatabaseTypes.I)
    def read_by_id(
        self, id: str, session: Optional[Session] = None, *args, **kwargs
    ) -> Tuple[T, Session]:
        """Read by ID operation"""
        if not session:
            raise Exception(ExceptionTypes.DB_SESSION_NOT_FOUND)
        return session.query(self.model).filter(self.model.id == id).one(), session

    @db_session(DatabaseTypes.I)
    def read(
        self, session: Optional[Session] = None, *args, **kwargs
    ) -> Tuple[List[T], Session]:
        """Read operation"""
        if not session:
            raise Exception(ExceptionTypes.DB_SESSION_NOT_FOUND)
        return session.query(self.model).all(), session

    @db_session(DatabaseTypes.I)
    def create(
        self, entity: T, session: Optional[Session] = None, *args, **kwargs
    ) -> Tuple[T, Session]:
        """Create operation"""
        if not session:
            raise Exception(ExceptionTypes.DB_SESSION_NOT_FOUND)
        model = (
            session.query(self.model).filter((self.model.id == entity.id)).one_or_none()
        )
        if not model:
            model = self.model(**entity.to_dict(exclude={"updated_at", "created_at"}))
            session.add(model)
            session.flush()
        return model, session

    @db_session(DatabaseTypes.I)
    def update(
        self, entity: T, session: Optional[Session] = None, *args, **kwargs
    ) -> Tuple[T, Session]:
        """Upsert operation"""
        if not session:
            raise Exception(ExceptionTypes.DB_SESSION_NOT_FOUND)
        LOGGER.info(entity.to_dict(exclude={"id"}))
        session.query(self.model).filter(self.model.id == entity.id).update(
            entity.to_dict(exclude={"updated_at", "created_at", "id"})
        )
        session.flush()
        if not entity.id:
            raise Exception(ExceptionTypes.ID_INVALID)
        return entity, session

    @db_session(DatabaseTypes.I)
    def delete(
        self, entity: T, session: Optional[Session] = None, *args, **kwargs
    ) -> Tuple[T, Session]:
        """Delete operation"""
        if not session:
            raise Exception(ExceptionTypes.DB_SESSION_NOT_FOUND)
        session.delete(entity)
        session.flush()
        return entity, session
