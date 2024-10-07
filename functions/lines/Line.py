from typing import Optional, List, Any

from functions.lines.LineElement import LineElement
from functions.settings.text_color.SchemeColor import SchemeColor


class Line:
    elements: List[LineElement]
    space_separated: bool
    header: Optional[LineElement]

    def __init__(
        self,
        elements: List[LineElement],
        space_separated=False,
        header: LineElement = None,
        color: SchemeColor = None,
        bold: bool = None,
    ):
        if color:
            for element in elements:
                element.color = color
        if bold is not None:
            for element in elements:
                element.bold = bold
        self.elements = elements
        self.space_separated = space_separated
        self.header = header

    def clone(self):
        return Line(self.elements[:], self.space_separated, self.header)

    def render(self, max_width: int):
        width_counter = 0
        for element in self.elements:
            width_counter = element.render(
                width_counter, max_width, self.space_separated
            )
        if width_counter < max_width:
            print()

    def is_empty(self):
        return len(self.elements) == 0

    @staticmethod
    def key_value(key: str, value: Any):
        return Line([LineElement(f"{key}: ", bold=True), LineElement(str(value))])

    @staticmethod
    def empty():
        return Line([])

    @staticmethod
    def simple(value: str, color: SchemeColor = None):
        return Line([LineElement(value, color)])

    @staticmethod
    def bold(value: str, color: SchemeColor = None):
        return Line([LineElement.bold(value, color)])

    @staticmethod
    def space_separated(elements: List[LineElement]):
        return Line(elements, space_separated=True)
