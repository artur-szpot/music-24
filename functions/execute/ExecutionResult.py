from typing import List, Optional

from functions.definition.ActionEnum import ActionEnum
from functions.execute.Line import Line
from functions.file_management.MusicFile import MusicFile
from functions.result_scrolling.CurrentPosition import CurrentPosition


class ExecutionResult:
    _action: ActionEnum
    _message: Line
    _error_message: Line
    _header: List[Line]
    _paginable: List[Line]
    _files: List[MusicFile]

    def __init__(
        self,
        action: ActionEnum,
        message: Line = None,
        error_message: Line = None,
        header: List[Line] = None,
        paginable: List[Line] = None,
        files: List[MusicFile] = None,
    ):
        self._action = action
        self._message = message
        self._error_message = error_message
        self._header = header
        self._paginable = paginable
        self._total_items = len(self._paginable or [])
        self._files = files

    def get_action(self) -> ActionEnum:
        return self._action

    def get_message(self) -> Line:
        return self._message

    def get_error_message(self) -> Line:
        return Line.simple( self._error_message)

    def get_total_items(self) -> int:
        return len(self._paginable or [])

    def get_item(self, index:int) -> Optional[ Line]:
        if self._paginable:
            return self._paginable[index]
        return None

    def get_file(self, index:int) -> Optional[ MusicFile]:
        if self._files:
            return self._files[index]
        return None

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
    def table(header:List[Line], items:List[Line], files:List[MusicFile]=None):
        return ExecutionResult(action=ActionEnum.Repeat, header=header, paginable=items, files=files)

    @staticmethod
    def paginable(items:List[Line]):
        return ExecutionResult(action=ActionEnum.Repeat, paginable=items)

    def render(
        self, current_position: CurrentPosition, error_message: Line = None
    ) -> List[Line]:
        contents = self.render_contents(current_position) or []
        if contents and error_message:
            contents.append(Line.empty())
        if error_message:
            contents.append(error_message)
        return contents or [Line.simple( "No result")]

    def render_contents(self, current_position: CurrentPosition) -> Optional[List[Line]]:
        if self._message:
            return [ self._message]
        if self._paginable:
            header = [current_position.render()]
            if self._header:
                header += self._header
            else:
                header.append(Line.empty())
            return (
                header
                + self._paginable[
                    current_position.first_item : current_position.last_item
                ]
            )
        return None
