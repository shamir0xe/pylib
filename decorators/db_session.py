import functools
import logging

from ..asynchrone.get_lock import GetLock
from ..database.actions.borrow_session import BorrowSession
from ..database.actions.release_session import ReleaseSession
from ..types.database_types import DatabaseTypes

LOGGER = logging.getLogger(__name__)


def db_session(db: DatabaseTypes):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            creation = False
            keep_alive: bool = (
                "db_session_keep_alive" in kwargs
                and kwargs["db_session_keep_alive"] is True
            )
            if "session" not in kwargs:
                with GetLock.threading_lock():
                    session = BorrowSession(database=db).borrow()
                    kwargs["session"] = session
                    creation = True
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                try:
                    LOGGER.info("Rolling transaction back")
                    kwargs["session"].rollback()
                except Exception as ee:
                    LOGGER.info(f"During rollback, {str(ee)} occurred")
                if creation:
                    ReleaseSession(database=db, session=kwargs["session"]).release()
                raise Exception(e)
            kwargs["session"].commit()
            if creation and not keep_alive:
                ReleaseSession(database=db, session=kwargs["session"]).release()
            return result

        return wrapper

    return decorator
