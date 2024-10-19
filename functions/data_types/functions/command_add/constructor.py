from typing import List

from functions.commands.print_command import print_command
from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.functions.command_add.definition import (
    add_definition,
)
from functions.data_types.functions.command_add.kwargs import AddKwargs


class AddCommand:
    @staticmethod
    def create(
        data_type: DataTypeEnum,
        name: str,
        aliases: List[str] = None,
        misspellings: List[str] = None,
    ) -> str:
        kwargs = []
        if aliases:
            kwargs.append({AddKwargs.Aliases: aliases})
        if misspellings:
            kwargs.append({AddKwargs.Misspellings: misspellings})
        return print_command(add_definition(data_type), args=[name], kwargs=kwargs)


class AddArtistCommand:
    @staticmethod
    def create(
        name: str,
        aliases: List[str] = None,
        misspellings: List[str] = None,
    ) -> str:
        return AddCommand.create(DataTypeEnum.ARTIST, name, aliases, misspellings)


class AddGenreCommand:
    @staticmethod
    def create(
        name: str,
        aliases: List[str] = None,
        misspellings: List[str] = None,
    ) -> str:
        return AddCommand.create(DataTypeEnum.GENRE, name, aliases, misspellings)
