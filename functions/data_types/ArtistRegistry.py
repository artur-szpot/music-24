from functions.data_types.Artist import Artist
from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.DataTypeRegistry import DataTypeRegistry


class ArtistRegistry(DataTypeRegistry[Artist]):

    @staticmethod
    def get_data_type():
        return Artist

    @staticmethod
    def get_data_type_name() -> str:
        return DataTypeEnum.ARTIST.value


# class ArtistRegistry:
#     artists: List[Artist]
#
#     def __init__(self):
#         try:
#             with open(f"db/data/artists.json", mode="r") as current_file:
#                 self.artists = [
#                     Artist.from_dict(value) for value in json.loads(current_file.read())
#                 ]
#         except:
#             self.artists = []
#
#     def find(self, name: str) -> Optional[Artist]:
#         for artist in self.artists:
#             if artist.name == name or name in artist.aliases:
#                 return artist
#
#     def add(self, new_artist: Artist) -> None:
#         self.artists.append(new_artist)
#         self.save()
#
#     def add_alias(self, alias: str, index: int = None, name: str = None):
#         artist: Optional[Artist] = None
#         if index is not None:
#             artist = self.artists[index]
#         elif name is not None:
#             artist = self.find(name)
#         if artist is None:
#             raise KeyError()
#         artist.aliases.append(alias)
#         self.save()  # todo make sure it works (modifies self.artists)
#
#     def save(self):
#         with open(f"db/data/artists.json", mode="w") as current_file:
#             json.dumps([artist.to_dict() for artist in self.artists])
