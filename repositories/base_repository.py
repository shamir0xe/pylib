from abc import ABC, abstractmethod
from typing import Generic, List, Tuple, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")
K = TypeVar("K")


class BaseRepository(ABC, Generic[T, K]):
    @abstractmethod
    def create(self, entity: T, *args, **kwargs) -> Tuple[T, Session]:
        pass

    @abstractmethod
    def update(self, entity: T, *args, **kwargs) -> Tuple[T, Session]:
        pass

    @abstractmethod
    def delete(self, entity: T, *args, **kwargs) -> Tuple[T, Session]:
        pass

    @abstractmethod
    def read_by_id(self, id: K, *args, **kwargs) -> Tuple[T, Session]:
        pass

    @abstractmethod
    def read(self, *args, **kwargs) -> Tuple[List[T], Session]:
        pass
