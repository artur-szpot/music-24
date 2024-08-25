import json
from typing import Any, Dict

from libs.io import create_directory

default_settings = {"page_size": 6, "some_setting": 0}


class AppSettings:
    page_size: int

    def __init__(self):
        self.apply_settings()

    def apply_settings(self, updated_settings: Dict[str, Any] = None) -> None:
        settings = {}
        try:
            with open(f"db/settings/settings.json", mode="r") as current_file:
                settings = json.loads(current_file.read())
        except:
            pass
        settings.update(updated_settings or {})
        get_settings = lambda name: settings.get(name, default_settings.get(name))

        self.page_size = get_settings("page_size")

    def save_settings(self) -> None:
        current_settings = {"page_size": self.page_size}
        new_settings = {
            key: value
            for key, value in current_settings.items()
            if default_settings.get(key) != value
        }
        create_directory("db/settings")
        with open("db/settings/settings.json", mode="w") as current_file:
            current_file.write(json.dumps(new_settings))

    def set(self, name: str, value: Any) -> None:
        if name in default_settings.keys():
            self.apply_settings({name: value})
        else:
            raise KeyError(f'Unknown setting name: "{name}".')
        self.save_settings()
