from __future__ import annotations
from typing import TypeVar

T = TypeVar("T", bound="DataTransferObject")


class DataTransferObject:
    def __init__(self, **kwargs) -> None:
        self.__dict__ = kwargs

    def from_dict(
        self: T,
        obj: dict,
    ) -> T:
        for key, _ in self.__dict__.items():
            if key in obj:
                data = obj[key]
                if hasattr(self, f"{key}_mapper"):
                    data = getattr(self, f"{key}_mapper")(data)
                setattr(self, key, data)
        return self

    def __str__(self) -> str:
        res = ""
        res += "*" * 11 + "\n"
        for key, value in self.__dict__.items():
            res += f"[{key}] = {value}\n"
        res += "*" * 11 + "\n"
        return res

    def add_attributes(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        return self.__dict__
