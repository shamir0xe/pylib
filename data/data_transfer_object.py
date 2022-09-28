from __future__ import annotations
from typing import Any


class DataTransferObject:
    def __init__(self, **kwargs: Any) -> None:
        self.__dict__ = kwargs

    @staticmethod
    def from_dict(obj: dict) -> DataTransferObject:
        data = DataTransferObject()
        for key, value in obj.items():
            setattr(data, key, value)
        return data

    def __str__(self) -> str:
        res = ''
        res += '*' * 11 + '\n'
        for key, value in self.__dict__.items():
            res += f'[{key}] = {value}\n'
        res += '*' * 11 + '\n'
        return res
    
    def add_attributes(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> dict:
        return self.__dict__
