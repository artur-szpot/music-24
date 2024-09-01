from enum import Enum

from functions.lines.SchemeColor import SchemeColor
from functions.lines.TextColor import TextColor


class ColorScheme(Enum):
    Dark = "dark"
    Light = "light"


def color_mapper(scheme: ColorScheme, color: SchemeColor) -> TextColor:
    try:
        if scheme == ColorScheme.Dark:
            value = (
                {
                    SchemeColor.GOOD: TextColor.GREEN,
                    SchemeColor.BAD: TextColor.RED,
                    SchemeColor.INFO: TextColor.YELLOW,
                }
                .get(color, color)
                .value
            )
        elif scheme == ColorScheme.Light:
            value = (
                {
                    SchemeColor.GOOD: TextColor.GREEN,
                    SchemeColor.BAD: TextColor.RED,
                    SchemeColor.INFO: TextColor.BLUE,
                }
                .get(color, color)
                .value
            )
        else:
            raise ValueError()
        return TextColor(value)
    except ValueError:
        return TextColor.MAGENTA
