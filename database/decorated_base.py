from typing import Dict, Set
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from ..string.generate_id import GenerateId
from ..utils.time.get_current_time import GetCurrentTime


class DecoratedBase(DeclarativeBase):
    updated_at: Mapped[datetime] = mapped_column(
        index=True,
        doc="Last Update Time",
        default=GetCurrentTime.get,
        onupdate=GetCurrentTime.get,
    )
    created_at: Mapped[datetime] = mapped_column(
        index=True, doc="Creation Time", default=GetCurrentTime.get
    )
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=GenerateId.generate,
    )

    def to_dict(self, exclude: Set[str] = set()) -> Dict:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column not in exclude
        }
