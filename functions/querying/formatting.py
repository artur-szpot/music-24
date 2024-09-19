from typing import Optional

from functions.lines.Line import LineElement
from functions.file_management.MusicFile import MusicFile
from functions.settings.text_color.SchemeColor import SchemeColor
from functions.querying.SpecialColumn import SpecialColumn
from functions.querying.View import ViewColumn


def format_special(music_file: MusicFile, column: ViewColumn) -> LineElement:
    if column.special == SpecialColumn.LENGTH:
        return format_length(music_file.length, column)
    if column.special == SpecialColumn.ORDINAL_NUMBER:
        return format_value(str(music_file.get_ordinal_number()), column)
    if column.special == SpecialColumn.ERRORS:
        value = format_value(str(len(music_file.errors)), column)
        if len(music_file.errors):
            value.set(color=SchemeColor.BAD, bold=True)
        return value
    if column.special == SpecialColumn.WARNINGS:
        value = format_value(str(len(music_file.warnings)), column)
        if len(music_file.warnings):
            value.set(color=SchemeColor.BAD, bold=True)
        return value
    raise KeyError(f"Special column formatting not handled: {column.special.value}")


def format_property(music_file: MusicFile, column: ViewColumn) -> LineElement:
    if column.special is not None:
        return format_special(music_file, column)
    value = music_file.to_dict().get(column.property_name)
    if isinstance(value, list):
        value = ", ".join(value)
    return format_value(value, column)


def format_value(value: Optional[str], column: ViewColumn) -> LineElement:
    if value is None:
        value = ""
    width = column.width
    trimmed_value = value[:width]
    padded_value = (
        trimmed_value.ljust(width)
        if not column.right_align
        else trimmed_value.rjust(width)
    )
    return LineElement(padded_value)


def format_length(length: Optional[int], column: ViewColumn = None) -> LineElement:
    if length is None:
        length = 0
    hours = length // 3600
    minutes = (length - hours * 3600) // 60
    seconds = length - hours * 3600 - minutes * 60
    pad = lambda num: str(num).rjust(2, "0")
    if not hours:
        length = f"{pad(minutes)}:{pad(seconds)}"
        if column and column.right_align:
            return LineElement(f"   {length}")
        else:
            return LineElement(length)
    return LineElement(f"{pad(hours)}:{pad(minutes)}:{pad(seconds)}")
