import logging
from typing import List, Tuple

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from ..mediators.engine_mediator import EngineMediator
from ..actions.create_database_session import CreateDatabaseSession
from ...types.database_types import DatabaseTypes
from ...types.exception_types import ExceptionTypes

LOGGER = logging.getLogger("[DbSessionMediator]")


class SessionMediator:
    database: DatabaseTypes
    engine: Engine
    sessions: List[Tuple[int, Session]]

    def __init__(self, database: DatabaseTypes) -> None:
        self.database = database
        self._precalc()

    def _precalc(self) -> None:
        self.sessions = []
        if self.database is DatabaseTypes.I:
            self.engine = EngineMediator().get(DatabaseTypes.I)
        elif self.database is DatabaseTypes.II:
            self.engine = EngineMediator().get(DatabaseTypes.II)
        elif self.database is DatabaseTypes.III:
            self.engine = EngineMediator().get(DatabaseTypes.III)
        elif self.database is DatabaseTypes.IV:
            self.engine = EngineMediator().get(DatabaseTypes.IV)
        elif self.database is DatabaseTypes.V:
            self.engine = EngineMediator().get(DatabaseTypes.V)
        elif self.database is DatabaseTypes.VI:
            self.engine = EngineMediator().get(DatabaseTypes.VI)
        elif self.database is DatabaseTypes.VII:
            self.engine = EngineMediator().get(DatabaseTypes.VII)
        elif self.database is DatabaseTypes.VIII:
            self.engine = EngineMediator().get(DatabaseTypes.VIII)
        elif self.database is DatabaseTypes.IX:
            self.engine = EngineMediator().get(DatabaseTypes.IX)
        elif self.database is DatabaseTypes.X:
            self.engine = EngineMediator().get(DatabaseTypes.X)
        elif self.database is DatabaseTypes.XI:
            self.engine = EngineMediator().get(DatabaseTypes.XI)
        elif self.database is DatabaseTypes.XII:
            self.engine = EngineMediator().get(DatabaseTypes.XII)
        else:
            # Invalid Database
            raise Exception(ExceptionTypes.DATABASE_INVALID)

    def have_any(self) -> bool:
        """Returns whether a session is already available"""
        if len(self.sessions) > 0 and self.sessions[0][0] == 1:
            return True
        return False

    def get(self) -> Session:
        """Fetch the available session, make it unavailable"""
        if not self.have_any():
            raise Exception(ExceptionTypes.DB_SESSION_NOT_AVAILABLE)
        _, session = self.sessions[0]
        self.sessions[0] = (0, session)
        self._sort_sessions()
        LOGGER.info(f"[{self.database.value}]: Using Session#{session.hash_key}")
        return session

    def _sort_sessions(self) -> None:
        self.sessions = sorted(self.sessions, key=lambda tup: -tup[0])

    def create(self) -> Session:
        """Create a new database session, make it unavailable"""
        session = CreateDatabaseSession.create(engine=self.engine)
        self.sessions += [(0, session)]
        LOGGER.info(
            f"[{self.database.value}]: New session have been created session#{session.hash_key}"
        )
        return session

    def release(self, session: Session) -> None:
        """Release the provided database session, make it available"""
        session.expunge_all()
        idx = -1
        for i, tup in enumerate(self.sessions):
            if isinstance(tup[1], Session) and tup[1].hash_key == session.hash_key:
                idx = i
                break
        if idx == -1:
            raise Exception(ExceptionTypes.DB_SESSION_NOT_FOUND)
        self.sessions[idx] = (1, self.sessions[idx][1])
        self._sort_sessions()
        LOGGER.info(
            f"[{self.database.value}]: Releasing the session#{session.hash_key}"
        )

    def close_all(self) -> None:
        """Closes and removes all the open sessions"""
        for database, session in self.sessions:
            try:
                session.close()
            except Exception as e:
                LOGGER.info(
                    f"Exception {e} occured during closing {database}'s session {session}"
                )
