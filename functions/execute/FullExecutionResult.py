from typing import Optional, List

from functions.commands.definition.FunctionDefinition import FunctionDefinition
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
        current_position.update()
        retval = [
            Line.empty(),
            (Line.empty() if self.message is None else self.message),
        ]
        if self.result is not None:
            retval.extend(self.result.render(current_position))
        else:
            retval.extend(
                [Line.empty() for i in range(current_position.terminal_size - 2)]
            )
        return retval
