from enum import Enum
from typing import Optional, List, Any

from termcolor import cprint


class TextColor(Enum):
    BLACK='black'
    GREEN='green'
    RED='red'
    YELLOW='yellow'
    GRAY='gray'
    BLUE='blue'
    MAGENTA='magenta'
    CYAN='cyan'
    LIGHT_GRAY='light_gray'
    DARK_GRAY='dark_gray'
    LIGHT_RED='light_red'
    LIGHT_BLUE='light_blue'
    LIGHT_YELLOW='light_yellow'
    LIGHT_GREEN='light_green'
    LIGHT_MAGENTA='light_magenta'
    LIGHT_CYAN='light_cyan'
    WHITE='white'


class LineElement:
    color: Optional[ TextColor]
    text: str
    bold: bool

    def __init__(self, text:Any, color:TextColor=None, bold:bool=False):
        self.text = str(text)
        self.color=color
        self.bold=bold

    def set(self,text:Any=None, color:TextColor=None, bold:bool=None):
        if text is not None:
            self.text = text
        if color is not None:
            self.color=color
        if bold is not None:
            self.bold=bold

    @staticmethod
    def bold(text:Any, color:TextColor=None):
        return LineElement(text, color=color, bold=True)

    def render(self,space_separated:bool=False):
        cprint(self.text,self.color.value if self.color else None, None, ["bold"] if self.bold else None, end=" " if space_separated else "")

class Line:
    elements: List[LineElement]
    space_separated:bool

    def __init__(self, elements: List[LineElement],space_separated=False):
        self.elements =elements
        self.space_separated=space_separated

    def render(self):
        for element in self.elements:
            element.render(self.space_separated)
        print()

    @staticmethod
    def key_value(key:str, value:Any):
        return Line([
            LineElement(f"{key}: ", bold=True),
            LineElement(str(value))
        ])

    @staticmethod
    def empty():
        return Line([])

    @staticmethod
    def simple(value:str, color:TextColor=None):
        return Line([LineElement(value,color)])

    @staticmethod
    def bold(value:str, color:TextColor=None):
        return Line([LineElement.bold(value,color)])

    @staticmethod
    def space_separated(elements: List[LineElement]):
        return Line(elements,space_separated=True)