from typing import Any
from dataclasses import dataclass
from ..file.file import File
from ..path.path_helper import PathHelper
from ..json.json_helper import JsonHelper


@dataclass
class Config:
    file_path: str = __file__
    file_format: str = ".json"
    folder_name: str = "configs"

    def get(self, filename: str, selector: str = "", default: Any = None) -> Any:
        json = File.read_json(
            PathHelper.from_root(
                self.file_path, self.folder_name, filename + self.file_format
            )
        )
        value = JsonHelper.selector_get_value(json, selector)
        if value != {}:
            return value
        return default

    def read(self, selector: str, **kwargs) -> Any:
        index = selector.find(".")
        if index < 0:
            filename = selector
            selector = ""
        else:
            filename = selector[:index]
            selector = selector[index + 1 :]
        return self.get(filename, selector, **kwargs)
