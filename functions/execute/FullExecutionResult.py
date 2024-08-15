from typing import Optional

from functions.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ExecutionResult import ExecutionResult


class FullExecutionResult:
    command: Optional[FunctionDefinition]
    result: Optional[ExecutionResult]
    error_message: Optional[str]

    def __init__(
        self,
        command: FunctionDefinition = None,
        result: ExecutionResult = None,
        error_message: Optional[str] = None,
    ):
        self.command = command
        self.result = result
        self.error_message = error_message
