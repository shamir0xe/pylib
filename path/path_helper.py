import os
from dataclasses import dataclass


@dataclass
class PathHelper:
    root_names: list[str] = ["src", "root"]

    def root_path(self) -> str:
        path = os.path.normpath(os.path.abspath(__file__))
        while str(os.path.dirname(path)) not in self.root_names:
            try:
                path = os.path.join(path, "..")
            except Exception:
                break
        res = ""
        try:
            res = os.path.normpath(os.path.join(path, ".."))
        except Exception:
            pass
        return res

    @staticmethod
    def from_root(*path, **kwargs) -> str:
        """
        assuming the arcitecture is like src/... or root/...,
        it'll go back till reach {src, root} folders
        """
        instance = PathHelper()
        if "root_name" in kwargs:
            instance = PathHelper([kwargs["root_name"]])
        return os.path.normpath(os.path.join(instance.root_path(), *path))
