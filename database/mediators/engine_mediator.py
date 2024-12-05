from typing import Dict
from sqlalchemy.engine import Engine
from ...decorators.singleton import singleton
from ...types.database_types import DatabaseTypes
from ...types.exception_types import ExceptionTypes


@singleton
class EngineMediator:
    def __init__(self) -> None:
        self.engines: Dict[str, Engine] = {}

    def get(self, database: DatabaseTypes) -> Engine:
        if database.value in self.engines:
            return self.engines[database.value]
        raise Exception(ExceptionTypes.DATABASE_INVALID)

    def register(self, database: DatabaseTypes, engine: Engine) -> None:
        self.engines[database.value] = engine
