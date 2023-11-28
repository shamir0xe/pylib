import os
import sys
from dataclasses import dataclass, field


@dataclass
class PathHelper:
    root_names: list[str] = field(default_factory=lambda: ["src", "root"])

    def root_path(self) -> str:
        path = os.path.normpath(os.path.abspath(sys.argv[0]))
        while os.path.basename(path) not in self.root_names:
            try:
                bef = path
                path = os.path.normpath(os.path.join(path, ".."))
                if path == bef:
                    break
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
