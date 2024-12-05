import time

from ...types.exception_types import ExceptionTypes
from ...types.time_formats import TimeFormats


class Timer:
    init_time: float

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.init_time = self._cur_time()

    def _cur_time(self) -> float:
        return time.time()

    def elapsed_time(self, time_format=TimeFormats.MIS) -> float:
        delta = self._cur_time() - self.init_time
        if time_format == TimeFormats.MIS:
            return delta * 10**3
        elif time_format == TimeFormats.MUS:
            return delta * 10**6
        elif time_format is TimeFormats.SEC:
            return delta
        elif time_format is TimeFormats.MIN:
            return delta / 60
        else:
            raise Exception(ExceptionTypes.TIME_FORMAT_NOT_SUPPORTED)
