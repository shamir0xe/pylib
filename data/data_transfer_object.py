from __future__ import annotations
from dataclasses import asdict, dataclass, fields


@dataclass
class DataTransferObject:
    def __init__(self, **kwargs) -> None:
        self.__dict__ = kwargs

    @classmethod
    def from_dict(
        cls,
        obj: dict,
    ):
        res: dict = {}
        field_names = [field.name for field in fields(cls)]
        for key, value in obj.items():
            if key in field_names:
                res[key] = value
        dto = cls(**res)
        for key, value in dto.__dict__.items():
            if hasattr(dto, f"{key}_mapper"):
                setattr(dto, key, getattr(dto, f"{key}_mapper")(value))
        return dto

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
        return asdict(self)
