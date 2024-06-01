from typing import Dict, List

from functions.file_management.MusicFile import MusicFile


class SpecialColumn:
    OrdinalNumber = 0
    Length = 1


class ViewColumn:
    label: str = "#"
    width: int = 10
    property_name: str = "#"
    right_align: bool = False
    special: SpecialColumn = None

    def __init__(self, source: Dict):
        self.label = source.get("label")
        self.width = source.get("width")
        self.property_name = source.get("property_name")
        self.special = source.get("special")
        self.right_align = source.get("right_align")
        if not self.property_name and self.special is None:
            raise ValueError(
                "Either property name or special needs to be set in a ViewColumn"
            )

    def to_dict(self) -> Dict:
        return {
            "label": self.label,
            "width": self.width,
            "property_name": self.property_name,
            "right_align": self.right_align,
        }


class ViewColumnSort:
    property_name: str = ""
    ascending: bool = True

    def __init__(self, property_name: str, ascending: bool = True):
        self.property_name = property_name
        self.ascending = ascending

    def to_dict(self) -> Dict:
        return {"property_name": self.property_name, "ascending": self.ascending}


class View:
    columns: List[ViewColumn] = []
    sort: List[ViewColumnSort] = []

    def __init__(self, source: Dict):
        self.columns = [ViewColumn(column) for column in source.get("columns", [])]
        self.sort = [
            ViewColumnSort(property_name, ascending)
            for property_name, ascending in source.get("sort", {}).items()
        ]

    def to_dict(self) -> Dict:
        return {
            "columns": [column.to_dict() for column in self.columns],
            "sort": [column.to_dict() for column in self.sort],
        }

    def print_file(self, music_file: MusicFile) -> str:
        return "  ".join(
            [format_property(music_file, column) for column in self.columns]
        )

    def line_length(self) -> int:
        return (
            sum(column.width for column in self.columns) + (len(self.columns) - 1) * 2
        )

    def print_separator_line(self) -> str:
        return self.line_length() * "="

    def print_title_line(self) -> str:
        return "  ".join(
            [format_value(column.label, column) for column in self.columns]
        )


def format_property(music_file: MusicFile, column: ViewColumn) -> str:
    if column.special == SpecialColumn.Length:
        return format_length(music_file.length)
    if column.special == SpecialColumn.OrdinalNumber:
        return format_value(str(music_file.get_ordinal_number()), column)
    value = music_file.to_dict().get(column.property_name)
    if isinstance(value, list):
        value = ", ".join(value)
    return format_value(value, column)


def format_value(value: str, column: ViewColumn) -> str:
    width = column.width
    trimmed_value = value[:width]
    padded_value = (
        trimmed_value.ljust(width)
        if not column.right_align
        else trimmed_value.rjust(width)
    )
    return padded_value


def format_length(length: int) -> str:
    hours = length // 3600
    minutes = (length - hours * 3600) // 60
    seconds = length - hours * 3600 - minutes * 60
    pad = lambda num: str(num).rjust(2, "0")
    if not hours:
        return f"   {pad(minutes)}:{pad(seconds)}"
    return f"{pad(hours)}:{pad(minutes)}:{pad(seconds)}"


standard_view = View(
    {
        "columns": [
            {
                "label": "no.",
                "width": 6,
                "right_align": True,
                "special": SpecialColumn.OrdinalNumber,
            },
            {
                "label": "length",
                "width": 8,
                "right_align": True,
                "special": SpecialColumn.Length,
            },
            {"label": "authors", "width": 70, "property_name": "authors"},
            {"label": "title", "width": 30, "property_name": "title"},
        ]
    }
)
