from typing import Protocol, runtime_checkable

from .additionable import Additionable
from .comparable import Comparable


@runtime_checkable
class ComparableAndAdditionabale(Comparable, Additionable, Protocol):
    pass
