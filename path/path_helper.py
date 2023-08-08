import os


DEFAULT_BACKWARD_TIMES = 3

class PathHelper:
    @staticmethod
    def root_path(backward_times: int) -> str:
        path = os.path.dirname(os.path.abspath(__file__))
        while backward_times > 0:
            backward_times -= 1
            path = os.path.join(path, "..")
        return path

    @staticmethod
    def from_root(*path, **kwargs) -> str:
        """
        assuming the arcitecture is like src/libs/pylib, 
        then depth should be 3
        """
        backward_times = DEFAULT_BACKWARD_TIMES
        if "backward_times" in kwargs:
            backward_times = kwargs["backward_times"]
        return os.path.normpath(
            os.path.join(PathHelper.root_path(backward_times), *path)
        )
