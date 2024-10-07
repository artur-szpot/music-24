import json
from typing import Any, Dict

from functions.settings.text_color.SchemeColor import SchemeColor
from functions.settings.text_color.TextColor import TextColor
from functions.settings.text_color.ColorScheme import ColorScheme, color_mapper
from libs.io import create_directory

PAGE_SIZE_AUTO = -1

default_settings = {
    "page_size": 12,  # todo cannot set lower than 10 (and lower than 12 = compact)
    "color_scheme": ColorScheme.Dark.value,
    "compact_table_header": False,
    "import_dir": "import",
    "storage_dir": "storage",
    "aliases": {"psa": "page-size --auto"},
}


class AppSettings:
    page_size: int
    color_scheme: ColorScheme
    compact_table_header: bool
    import_dir: str
    storage_dir: str
    aliases: Dict[str, str]

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
        self.compact_table_header = get_settings("compact_table_header")
        self.import_dir = get_settings("import_dir")
        self.storage_dir = get_settings("storage_dir")
        self.aliases = get_settings("aliases")

    def save_settings(self) -> None:
        current_settings = {
            "page_size": self.page_size,
            "color_scheme": self.color_scheme.value,
            "compact_table_header": self.compact_table_header,
            "import_dir": self.import_dir,
            "storage_dir": self.storage_dir,
            "aliases": self.aliases,
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

    def page_size_string(self) -> str:
        if self.page_size == PAGE_SIZE_AUTO:
            return "automatic"
        return str(self.page_size)
