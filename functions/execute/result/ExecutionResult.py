from typing import List, Optional

from functions.commands.definition.ActionEnum import ActionEnum
from functions.commands.definition.FunctionFollowingCommands import (
    FunctionFollowingCommands,
)
from functions.execute.result.ExecutionResultCategory import ExecutionResultCategory
from functions.lines.Line import Line
from functions.music_file.MusicFile import MusicFile
from functions.result_scrolling.CurrentPosition import CurrentPosition
from functions.settings.text_color.SchemeColor import SchemeColor


class ExecutionResult:
    _action: ActionEnum
    category: ExecutionResultCategory
    is_table: bool

    following_commands: Optional[FunctionFollowingCommands]
    _message: Optional[Line]
    _header: Optional[List[Line]]
    _paginable: Optional[List[Line]]
    _files: Optional[List[MusicFile]]

    def __init__(
        self,
        action: ActionEnum,
        category: ExecutionResultCategory,
        message: Line = None,
        header: List[Line] = None,
        paginable: List[Line] = None,
        files: List[MusicFile] = None,
        following_commands: Optional[FunctionFollowingCommands] = None,
        is_table: bool = False,
    ):
        self._action = action
        self.category = category
        self._message = message
        self._header = header
        self._paginable = paginable
        self._total_items = len(self._paginable or [])
        self._files = files
        self.is_table = is_table
        self.following_commands = following_commands

    def get_action(self) -> ActionEnum:
        return self._action

    def get_message(self) -> Line:
        return self._message or Line.empty()

    def set_message(self, message: str) -> None:
        self._message = Line.simple(message)

    def set_error_message(self, message: str) -> None:
        self._message = Line.simple(message, SchemeColor.BAD)

    def get_total_items(self) -> int:
        return len(self._paginable or [])

    def get_item(self, index: int) -> Optional[Line]:
        if self._paginable:
            return self._paginable[index]
        return None

    def get_file(self, index: int) -> Optional[MusicFile]:
        if self._files:
            return self._files[index]
        return None

    @staticmethod
    def action(action: ActionEnum):
        return ExecutionResult(action=action, category=ExecutionResultCategory.Action)

    @staticmethod
    def refresh():
        return ExecutionResult(
            action=ActionEnum.Refresh, category=ExecutionResultCategory.Action
        )

    @staticmethod
    def message(message: str):
        return ExecutionResult(
            action=ActionEnum.Repeat,
            message=Line.simple(message, color=SchemeColor.GOOD),
            category=ExecutionResultCategory.Message,
        )

    @staticmethod
    def error_message(message: str):
        # print(message)
        # quit()
        return ExecutionResult(
            action=ActionEnum.Refresh,
            message=Line.simple(message, color=SchemeColor.BAD),
            category=ExecutionResultCategory.Message,
        )

    @staticmethod
    def table(header: List[Line], items: List[Line], files: List[MusicFile] = None):
        return ExecutionResult(
            action=ActionEnum.Repeat,
            category=ExecutionResultCategory.Query,
            header=header,
            paginable=items,
            files=files,
            is_table=True,
        )

    @staticmethod
    def paginable(items: List[Line], header: List[Line] = None):
        return ExecutionResult(
            action=ActionEnum.Repeat,
            category=ExecutionResultCategory.Detail,
            paginable=items,
            header=header,
        )

    def render(self, current_position: CurrentPosition) -> List[Line]:
        return self.render_contents(current_position) or [Line.simple("No result")]

    def render_contents(
        self, current_position: CurrentPosition
    ) -> Optional[List[Line]]:
        # if self._message:
        #     return [self._message]
        if self._paginable:
            if self.is_table:
                header = [current_position.render_pagination()]
                if self._header:
                    header += self._header
            else:
                if self._header:
                    modified_header = self._header[0].clone()
                    modified_header.elements.extend(
                        current_position.render_pagination().elements
                    )
                    header = [modified_header] + self._header[1:] + [Line.empty()]
                else:
                    header = [current_position.render_pagination(), Line.empty()]
            items = self._paginable[
                current_position.first_item : current_position.last_item
            ]
            items.extend(
                [Line.empty() for i in range(current_position.page_size - len(items))]
            )
            return header + items
        return None
