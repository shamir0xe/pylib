from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..file.file import File
from ..json.json_helper import JsonHelper


@dataclass
class Config:
    filename: str
    home_path: List[str] = field(
        default_factory=lambda: [os.path.normpath(os.path.abspath(os.sep))]
    )
    json: Dict = field(default_factory=dict)
    folders: List[str] = field(default_factory=list)
    base_path: str = field(default_factory=os.getcwd)

    def recurse(self) -> Config:
        found = False
        path = self.base_path
        filename = self.filename
        try:
            while not found:
                if path in self.home_path:
                    raise Exception
                found = True
                try:
                    path_array = list(
                        filter(
                            lambda t: isinstance(t, str) and t,
                            [path, *self.folders, f"{filename}.json"],
                        )
                    )
                    cur_path = os.path.join(*path_array)
                    # print(f"reading {cur_path}")
                    if not os.path.isfile(cur_path):
                        raise Exception("not a valid file")
                    self.json = File.read_json(cur_path)
                except Exception:
                    path = os.path.abspath(os.path.normpath(os.path.join(path, "..")))
                    found = False
        except Exception:
            print(f"Please provide a local {self.base_path}/{filename}.json file")
            exit(0)
        return self

    def get(self, selector: str = "", default: Any = None) -> Any:
        value = JsonHelper.selector_get_value(self.json, selector)
        if value != {}:
            return value
        return default

    @staticmethod
    def read(
        selector: str, base_path: Optional[str] = None, home_path: Optional[str] = None
    ) -> Any:
        idx = -1
        try:
            idx = selector.index(".")
        except ValueError:
            pass
        if idx >= 0:
            filename = selector[:idx]
            selector = selector[idx + 1 :]
        else:
            filename = selector
            selector = ""
        kwargs = {}
        kwargs["filename"] = filename
        kwargs["folders"] = ["configs"]
        kwargs = {**kwargs, **Config.extract_args(base_path, home_path)}
        return Config(**kwargs).recurse().get(selector)

    @staticmethod
    def extract_args(
        base_path: Optional[str] = None, home_path: Optional[str] = None
    ) -> Dict:
        kwargs = {}
        if base_path:
            base_path = os.path.abspath(base_path)
            if os.path.isfile(base_path):
                base_path = os.path.dirname(base_path)
            kwargs["base_path"] = base_path
        if home_path:
            kwargs["home_path"] = home_path
        return kwargs

    @staticmethod
    def read_env(
        selector: str, base_path: Optional[str] = None, home_path: Optional[str] = None
    ) -> Any:
        kwargs = {"filename": "env", **Config.extract_args(base_path, home_path)}
        return Config(**kwargs).recurse().get(selector)
