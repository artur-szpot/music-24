from typing import Optional

from functions.file_management.MusicFile import MusicFile
from functions.querying.SpecialColumn import SpecialColumn
from functions.querying.View import ViewColumn


def format_special(music_file: MusicFile, column: ViewColumn) -> str:
    if column.special == SpecialColumn.LENGTH:
        return format_length(music_file.length)
    if column.special == SpecialColumn.ORDINAL_NUMBER:
        return format_value(str(music_file.get_ordinal_number()), column)
    if column.special == SpecialColumn.ERRORS:
        return format_value(str(len(music_file.errors)), column)
    raise KeyError(f"Special column formatting not handled: {column.special.value}")


def format_property(music_file: MusicFile, column: ViewColumn) -> str:
    if column.special is not None:
        return format_special(music_file, column)
    value = music_file.to_dict().get(column.property_name)
    if isinstance(value, list):
        value = ", ".join(value)
    return format_value(value, column)


def format_value(value: Optional[str], column: ViewColumn) -> str:
    if value is None:
        value = ""
    width = column.width
    trimmed_value = value[:width]
    padded_value = (
        trimmed_value.ljust(width)
        if not column.right_align
        else trimmed_value.rjust(width)
    )
    return padded_value


def format_length(length: Optional[int]) -> str:
    if length is None:
        length = 0
    hours = length // 3600
    minutes = (length - hours * 3600) // 60
    seconds = length - hours * 3600 - minutes * 60
    pad = lambda num: str(num).rjust(2, "0")
    if not hours:
        return f"   {pad(minutes)}:{pad(seconds)}"
    return f"{pad(hours)}:{pad(minutes)}:{pad(seconds)}"
