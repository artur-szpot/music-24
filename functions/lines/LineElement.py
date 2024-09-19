from typing import Optional, Any

import colorama
from termcolor import cprint

from functions.settings.text_color.SchemeColor import SchemeColor
from functions.settings.app_settings import app_settings

colorama.init()


class LineElement:
    color: Optional[SchemeColor]
    text: str
    bold: bool

    def __init__(self, text: Any, color: SchemeColor = None, bold: bool = False):
        self.text = str(text)
        self.color = color
        self.bold = bold

    def set(self, text: Any = None, color: SchemeColor = None, bold: bool = None):
        if text is not None:
            self.text = text
        if color is not None:
            self.color = color
        if bold is not None:
            self.bold = bold

    @staticmethod
    def bold(text: Any, color: SchemeColor = None):
        return LineElement(text, color=color, bold=True)

    def render(
        self,
        width_counter: int,
        max_width: int,
        space_separated: bool = False,
    ) -> int:
        if width_counter >= max_width:
            return width_counter
        text = self.text
        if space_separated:
            text += " "
        if width_counter + len(text) > max_width:
            text = text[: max_width - width_counter - 3] + "..."
        cprint(
            text,
            app_settings.color_mapper(self.color).value if self.color else None,
            None,
            ["bold"] if self.bold else None,
            end="",
        )
        return width_counter + len(text)
