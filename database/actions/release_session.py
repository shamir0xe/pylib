from dataclasses import dataclass
from sqlalchemy.orm import Session

from ...database.session_pools import SessionPools
from ...types.database_types import DatabaseTypes


@dataclass
class ReleaseSession:
    database: DatabaseTypes
    session: Session

    def release(self) -> None:
        SessionPools().release(database=self.database, session=self.session)
