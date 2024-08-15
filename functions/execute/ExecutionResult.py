from typing import List, Optional

from functions.definition.ActionEnum import ActionEnum
from functions.result_scrolling.CurrentPosition import CurrentPosition


class ExecutionResult:
    _action: ActionEnum
    _message: str
    _error_message: str
    _header: List[str]
    _paginable: List[str]

    def __init__(
        self,
        action: ActionEnum,
        message: str = None,
        error_message: str = None,
        header: List[str] = None,
        paginable: List[str] = None,
    ):
        self._action = action
        self._message = message
        self._error_message = error_message
        self._header = header
        self._paginable = paginable
        self._total_items = len(self._paginable or [])

    def get_action(self) -> ActionEnum:
        return self._action

    def get_message(self) -> str:
        return self._message

    def get_error_message(self) -> str:
        return self._error_message

    def get_total_items(self) -> int:
        return len(self._paginable or [])

    @staticmethod
    def action(action):
        return ExecutionResult(action=action)

    @staticmethod
    def message(message):
        return ExecutionResult(
            action=ActionEnum.Repeat,
            message=message,
        )

    @staticmethod
    def error_message(message):
        return ExecutionResult(
            action=ActionEnum.Repeat,
            error_message=message,
        )

    @staticmethod
    def table(header, items):
        return ExecutionResult(action=ActionEnum.Repeat, header=header, paginable=items)

    def render(
        self, current_position: CurrentPosition, error_message: str = None
    ) -> List[str]:
        contents = self.render_contents(current_position) or []
        if contents and error_message:
            contents.append("")
        if error_message:
            contents.append(error_message)
        return contents or ["No result"]

    def render_contents(self, current_position: CurrentPosition) -> Optional[List[str]]:
        if self._message:
            return [self._message]
        if self._paginable:
            header = [current_position.render()]
            if self._header:
                header += self._header
            return (
                header
                + self._paginable[
                    current_position.first_item : current_position.last_item
                ]
            )
        return None
