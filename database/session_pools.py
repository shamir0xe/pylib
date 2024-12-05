from typing import Dict, Optional
import logging

from sqlalchemy.orm import Session

from .mediators.session_mediator import SessionMediator
from ..decorators.singleton import singleton
from ..types.database_types import DatabaseTypes
from ..types.exception_types import ExceptionTypes

LOGGER = logging.getLogger(__name__)


@singleton
class SessionPools:
    def __init__(self) -> None:
        self.pool: Dict[DatabaseTypes, SessionMediator] = {}

    def get(self, database: DatabaseTypes) -> Optional[Session]:
        """Returns a session for the given {database} if it finds any
        available one or None instead"""
        if database in self.pool and self.pool[database].have_any():
            return self.pool[database].get()
        return None

    def create(self, database: DatabaseTypes) -> Session:
        """Creates a session for the given {database}"""
        if database not in self.pool:
            self.pool[database] = SessionMediator(database=database)
        return self.pool[database].create()

    def release(self, database: DatabaseTypes, session: Session) -> None:
        """Releases the given {session}"""
        if database not in self.pool:
            raise Exception(ExceptionTypes.DATABASE_INVALID)
        try:
            self.pool[database].release(session=session)
        except:
            LOGGER.info(
                f"Got an exception in releasing the session from\
                {database.value} #{session.hash_key}"
            )

    def close_all(self) -> None:
        for _, mediator in self.pool.items():
            mediator.close_all()
