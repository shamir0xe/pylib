from sqlalchemy import Engine
from sqlalchemy.orm import scoped_session, sessionmaker


class CreateDatabaseSession:
    @staticmethod
    def create(engine: Engine):
        Session = sessionmaker(bind=engine, expire_on_commit=False)
        scoped_session_factory = scoped_session(Session)
        return scoped_session_factory()
