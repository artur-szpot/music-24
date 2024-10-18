from typing import Optional, List

from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.result.ExecutionResult import ExecutionResult
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
        retval = []
        # todo reinstate message display
        # retval = [
        #     (Line.empty() if self.message is None else self.message),
        #     Line.empty(),
        # ]
        if self.result is not None:
            retval.extend(self.result.render(current_position))
        else:
            # allow 2 for top message and 2 for input line with break # todo 2 currently removed from the top
            retval.extend(
                [Line.empty() for i in range(current_position.terminal_size - 3)]
                # + [Line.empty() if self.message is None else self.message]
                # [Line.empty() for i in range(current_position.terminal_size - 4)]
            )
        retval.append(Line.empty())
        retval.append(Line.empty() if self.message is None else self.message)
        return retval
