import os


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
        assuming the arcitecture is like src/libs/python_library, 
        then depth should be 4
        """
        backward_times = 4
        if "backward_times" in kwargs:
            backward_times = kwargs["backward_times"]
        return os.path.normpath(
            os.path.join(PathHelper.root_path(backward_times), *path)
        )
