from enum import Enum


class ActionEnum(Enum):
    Return = 0  # exit the app
    Repeat = 1  # ask for next input
    Refresh = 2  # keep last command, only view has been changed
