import os
from dataclasses import dataclass, field


@dataclass
class PathHelper:
    file_path: str
    root_names: list[str] = field(default_factory=lambda: ["src", "root"])

    def root_path(self) -> str:
        path = os.path.normpath(os.path.abspath(self.file_path))
        while os.path.basename(path) not in self.root_names:
            try:
                bef = path
                path = PathHelper.backward(path)
                if path == bef:
                    break
            except Exception:
                break
        res = ""
        try:
            res = PathHelper.backward(path)
        except Exception:
            pass
        return res

    @staticmethod
    def from_root(file_path: str, *path: str, **kwargs) -> str:
        """
        assuming the arcitecture is like src/... or root/...,
        it'll go back till reach {src, root} folders
        """
        instance: PathHelper
        if "root_name" in kwargs:
            instance = PathHelper(file_path, [kwargs["root_name"]])
        else:
            instance = PathHelper(file_path)
        return os.path.normpath(os.path.join(instance.root_path(), *path))

    @staticmethod
    def backward(path: str) -> str:
        return os.path.normpath(os.path.join(path, ".."))
