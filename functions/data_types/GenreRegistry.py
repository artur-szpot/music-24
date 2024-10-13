from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.DataTypeRegistry import DataTypeRegistry
from functions.data_types.Genre import Genre


class GenreRegistry(DataTypeRegistry[Genre]):

    @staticmethod
    def get_data_type():
        return Genre

    @staticmethod
    def get_data_type_name() -> str:
        return DataTypeEnum.GENRE.value

    def check_specific(self, new_datum: Genre) -> None:
        incorrect = []
        for alias in [new_datum.name] + new_datum.aliases:
            if Genre.check_capitalization(alias):
                incorrect.append(alias)
        if len(incorrect):
            raise ValueError(
                f"Incorrect capitalization in the following "
                f"genre{'s' if len(incorrect) > 1 else ''}: {', '.join(incorrect)}")
