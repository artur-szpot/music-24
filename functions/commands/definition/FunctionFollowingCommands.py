from typing import Optional, List, Union

from libs.list_union_util import SimpleList, simple_list


class FollowingCommand:
    command_stack: List[str]

    def __init__(self, command_stack: SimpleList[str]):
        self.command_stack = simple_list(command_stack)


class FunctionFollowingCommands:
    # Command to use if enter is pressed without typing after the command had been executed.
    _empty_command: Optional[FollowingCommand]
    # Command to use if space is pressed before typing anything else after the command had been executed.
    _space_command: Optional[FollowingCommand]
    # Command to use if tab is pressed before typing anything else after the command had been executed.
    _tab_command: Optional[FollowingCommand]
    # Command to prepend to the user input if it does not begin with a known command.
    _default_command_prefix: Optional[str]

    def __init__(
            self,
            empty_command: Optional[FollowingCommand] = None,
            space_command: Optional[FollowingCommand] = None,
            tab_command: Optional[FollowingCommand] = None,
            default_prefix: Optional[str] = None,
    ):
        self._empty_command = empty_command
        self._space_command = space_command
        self._tab_command = tab_command
        self._default_command_prefix = default_prefix

    def empty(self, command_stack: SimpleList[str]):
        self._empty_command = FollowingCommand(command_stack)
        return self

    def space(self, command_stack: SimpleList[str]):
        self._space_command = FollowingCommand(command_stack)
        return self

    def tab(self, command_stack: SimpleList[str]):
        self._tab_command = FollowingCommand(command_stack)
        return self

    def default_prefix(self, command_prefix: str):
        self._default_command_prefix = command_prefix
        return self

    def get_empty(self) -> Optional[List[str]]:
        if self._empty_command is None:
            return None
        return self._empty_command.command_stack

    def get_space(self) -> Optional[List[str]]:
        if self._space_command is None:
            return None
        return self._space_command.command_stack

    def get_tab(self) -> Optional[List[str]]:
        if self._tab_command is None:
            return None
        return self._tab_command.command_stack

    def get_default(self) -> Optional[str]:
        return self._default_command_prefix
