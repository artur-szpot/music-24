from enum import Enum

from functions.settings.text_color.SchemeColor import SchemeColor
from functions.settings.text_color.TextColor import TextColor


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
                    SchemeColor.WARN: TextColor.YELLOW,
                    SchemeColor.BASE: TextColor.WHITE,
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
                    SchemeColor.WARN: TextColor.MAGENTA,
                    SchemeColor.BASE: TextColor.BLACK,
                }
                .get(color, color)
                .value
            )
        else:
            raise ValueError()
        return TextColor(value)
    except ValueError:
        return TextColor.MAGENTA
