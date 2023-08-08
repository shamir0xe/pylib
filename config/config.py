from typing import Any
from ..file.file import File
from ..path.path_helper import PathHelper
from ..json.json_helper import JsonHelper


DEFAULT_BACKWARD_TIMES = 3
DEFAULT_CONFIG_FOLDER_NAME = "configs"


class Config:
    def __init__(
        self,
        filename: str,
        backward_times: int = DEFAULT_BACKWARD_TIMES,
        config_folder_name: str = DEFAULT_CONFIG_FOLDER_NAME,
    ) -> None:
        filename += ".json"
        self.json = File.read_json(
            PathHelper.from_root(
                config_folder_name, filename, backward_times=backward_times
            )
        )

    def get(self, selector: str = "", default: Any = None) -> Any:
        value = JsonHelper.selector_get_value(self.json, selector)
        if value != {}:
            return value
        return default

    @staticmethod
    def read(selector: str, **kwargs) -> Any:
        index = selector.find(".")
        if index < 0:
            return Config(selector).get(**kwargs)
        filename = selector[:index]
        selector = selector[index + 1 :]
        return Config(filename).get(selector, **kwargs)
