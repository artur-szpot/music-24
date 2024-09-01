import json
from typing import Any, Dict

from functions.lines.SchemeColor import SchemeColor
from functions.lines.TextColor import TextColor
from functions.settings.ColorScheme import ColorScheme, color_mapper
from libs.io import create_directory

default_settings = {"page_size": 6, "color_scheme": ColorScheme.Dark.value}


class AppSettings:
    page_size: int
    color_scheme: ColorScheme

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
        self.color_scheme = ColorScheme(get_settings("color_scheme"))

    def save_settings(self) -> None:
        current_settings = {
            "page_size": self.page_size,
            "color_scheme": self.color_scheme.value,
        }
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

    def color_mapper(self, color: SchemeColor) -> TextColor:
        return color_mapper(self.color_scheme, color)
