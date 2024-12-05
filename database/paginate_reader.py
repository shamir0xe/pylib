import logging
from dataclasses import dataclass
from sqlalchemy.orm import Session
from typing import Generic, List, Type, TypeVar


LOGGER = logging.getLogger(__name__)
T = TypeVar("T")


@dataclass
class PaginateReader(Generic[T]):
    """
    Reading the elements of the given {model} sorted by
    it's {.id} property
    """

    model: Type[T]
    session: Session
    page_size: int
    total_records: int
    cur_page: int = 0

    @property
    def available(self) -> bool:
        return self.cur_page * self.page_size < self.total_records

    def next(self) -> List[T]:
        if not self.available:
            return []
        # Free the memory usage of the session
        self.session.expunge_all()
        LOGGER.info(
            f"Page #{self.cur_page+1}/{(self.total_records-1) // self.page_size+1}"
        )
        res = (
            self.session.query(self.model)
            .order_by(self.model.id)  # type: ignore
            .offset(self.cur_page * self.page_size)
            .limit(self.page_size)
            .all()
        )
        self.cur_page += 1
        return res
