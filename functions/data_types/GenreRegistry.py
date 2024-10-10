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


# class GenreRegistry:
#     genres: List[Genre]
#
#     def __init__(self):
#         try:
#             with open(f"db/data/genres.json", mode="r") as current_file:
#                 self.genres = [
#                     Genre.from_dict(value) for value in json.loads(current_file.read())
#                 ]
#         except:
#             self.genres = []
#
#     def find(self, name: str) -> Optional[Genre]:
#         for genre in self.genres:
#             if genre.name == name or name in genre.aliases:
#                 return genre
#
#     def add(self, new_genre: Genre) -> None:
#         self.genres.append(new_genre)
#         self.save()
#
#     def add_alias(self, alias: str, index: int = None, name: str = None):
#         genre: Optional[Genre] = None
#         if index is not None:
#             genre = self.genres[index]
#         elif name is not None:
#             genre = self.find(name)
#         if genre is None:
#             raise KeyError()
#         genre.aliases.append(alias)
#         self.save()  # todo make sure it works (modifies self.genres)
#
#     def save(self):
#         with open(f"db/data/genres.json", mode="w") as current_file:
#             current_file.write(json.dumps([genre.to_dict() for genre in self.genres]))
