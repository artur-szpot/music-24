from typing import Dict, List, Optional

from functions.file_management.MusicFile import MusicFile
from functions.querying.ViewColumn import ViewColumn
from functions.querying.ViewColumnSort import ViewColumnSort
from functions.querying.formatting import format_value, format_property


class View:
    columns: List[ViewColumn]
    sort: Optional[List[ViewColumnSort]]

    def __init__(self, columns: List[ViewColumn], sort: List[ViewColumnSort] = None):
        self.columns = columns
        self.sort = sort

    @staticmethod
    def from_dict(source: Dict):
        columns = [ViewColumn(column) for column in source.get("columns", [])]
        sort = [
            ViewColumnSort(property_name, ascending)
            for property_name, ascending in source.get("sort", {}).items()
        ]
        return View(columns, sort)

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
