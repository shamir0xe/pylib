"""
ATTENTION:
    DEPRECATED,
    use pydantic
"""

from __future__ import annotations
from dataclasses import asdict, dataclass, fields
from typing import Any, Dict


@dataclass
class DataTransferObject:
    """
    A generic data transfer object.
    """

    def __init__(self, **kwargs: Any) -> None:
        self.__dict__ = kwargs

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]):
        """
        Constructs an instance of the class from a dictionary.
        """
        dto_kwargs = {}
        field_names = {field.name for field in fields(cls)}
        for key, value in obj.items():
            if key in field_names:
                mapper_func = getattr(cls, f"{key}_mapper", None)
                if callable(mapper_func):
                    dto_kwargs[key] = mapper_func(value)
                else:
                    dto_kwargs[key] = value
        dto = cls(**dto_kwargs)
        return dto

    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        """
        attributes = "\n".join(
            [f"[{key}] = {value}" for key, value in self.__dict__.items()]
        )
        return f"************\n{attributes}\n************"

    def add_attributes(self, **kwargs: Any) -> None:
        """
        Dynamically adds attributes to the object.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dictionary.
        """
        return asdict(self)
