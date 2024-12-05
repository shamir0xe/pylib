import logging
from sqlalchemy import Engine, create_engine

from ..infos.postgres_database_info import PostgresDatabaseInfo
from ..decorated_base import DecoratedBase
from ...decorators.singleton import singleton
from ...config.config import Config

LOGGER = logging.getLogger("[PG_ENGINE]")


@singleton
class PostgresEngine:
    engine: Engine

    def __init__(self) -> None:
        postgres_data = PostgresDatabaseInfo(**Config.read_env("db.postgres"))
        LOGGER.info(postgres_data)
        self.engine = create_engine(
            url="postgresql+psycopg://{}:{}@{}:{}/{}".format(
                postgres_data.user,
                postgres_data.password,
                postgres_data.host,
                postgres_data.port,
                postgres_data.db,
            ),
            echo=False,
            pool_pre_ping=True,
        )
        DecoratedBase.metadata.create_all(self.engine)
