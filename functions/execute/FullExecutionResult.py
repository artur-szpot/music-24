from typing import Optional, List

from functions.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ExecutionResult import ExecutionResult
from functions.lines.Line import Line
from functions.result_scrolling.CurrentPosition import CurrentPosition


class FullExecutionResult:
    command: Optional[FunctionDefinition]
    result: Optional[ExecutionResult]
    message: Optional[Line]

    def __init__(
        self,
        command: FunctionDefinition = None,
        result: ExecutionResult = None,
        message: Optional[Line] = None,
    ):
        self.command = command
        self.result = result
        self.message = message

    def render(self, current_position: CurrentPosition) -> List[Line]:
        retval = []
        current_position.update()
        if self.result is not None:
            retval = self.result.render(current_position)
        if self.message is not None:
            if retval:
                retval.append(Line.empty())
            retval.append(self.message)
        return retval
