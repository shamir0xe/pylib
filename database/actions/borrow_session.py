from dataclasses import dataclass

from sqlalchemy.orm import Session

from ...database.session_pools import SessionPools
from ...types.database_types import DatabaseTypes


@dataclass
class BorrowSession:
    database: DatabaseTypes

    def borrow(self) -> Session:
        session = SessionPools().get(database=self.database)
        if session:
            return session
        return SessionPools().create(database=self.database)
