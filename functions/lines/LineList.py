from typing import List

from functions.lines.Line import Line
from functions.lines.LineElement import LineElement


class LineList:
    @staticmethod
    def list(lines: List[Line], header: LineElement):
        retval = [Line(elements=[header])]
        for line in lines:
            elements_with_bullet = [LineElement(" • ")]
            elements_with_bullet.extend(line.elements)
            line.elements = elements_with_bullet
            line.header = header
            retval.append(line)
        return retval
