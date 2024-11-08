from functions.commands.print_command import print_command
from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.functions.command_add_variant.verbs import add_variant_verbs


class AddVariantCommand:
    @staticmethod
    def create(
        data_type: DataTypeEnum, alias: bool, original: str, new_alias: str
    ) -> str:
        return print_command(
            add_variant_verbs(data_type, alias), args=[original, new_alias]
        )


class AddArtistAliasCommand:
    @staticmethod
    def create(original: str, alias: str) -> str:
        return AddVariantCommand.create(DataTypeEnum.ARTIST, True, original, alias)


class AddGenreAliasCommand:
    @staticmethod
    def create(original: str, alias: str) -> str:
        return AddVariantCommand.create(DataTypeEnum.GENRE, True, original, alias)


class AddArtistMisspellingCommand:
    @staticmethod
    def create(original: str, alias: str) -> str:
        return AddVariantCommand.create(DataTypeEnum.ARTIST, False, original, alias)


class AddGenreMisspellingCommand:
    @staticmethod
    def create(original: str, alias: str) -> str:
        return AddVariantCommand.create(DataTypeEnum.GENRE, False, original, alias)
