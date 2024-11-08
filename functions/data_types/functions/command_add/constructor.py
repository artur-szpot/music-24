from typing import List

from functions.commands.print_command import print_command
from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.Genre import GenreCategory
from functions.data_types.functions.command_add.kwargs import AddKwargs
from functions.data_types.functions.command_add.verbs import add_verbs


class AddCommand:
    @staticmethod
    def create(
        data_type: DataTypeEnum,
        name: str,
        aliases: List[str] = None,
        misspellings: List[str] = None,
        category: str = None,
    ) -> str:
        kwargs = []
        if aliases:
            kwargs.append({AddKwargs.Aliases: aliases})
        if misspellings:
            kwargs.append({AddKwargs.Misspellings: misspellings})
        if category:
            kwargs.append({AddKwargs.Category: category})
        return print_command(add_verbs(data_type), args=[name], kwargs=kwargs)


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
        category: GenreCategory,
        aliases: List[str] = None,
        misspellings: List[str] = None,
    ) -> str:
        return AddCommand.create(
            DataTypeEnum.GENRE, name, aliases, misspellings, category=category.value
        )
