import json
from typing import Optional, List

from functions.data_types.Genre import Genre


class GenreRegistry:
    genres: List[Genre]

    def __init__(self):
        try:
            with open(f"db/data/genres.json", mode="r") as current_file:
                self.genres = [
                    Genre.from_dict(value) for value in json.loads(current_file.read())
                ]
        except:
            self.genres = []

    def find_genre(self, name: str) -> Optional[Genre]:
        for genre in self.genres:
            if genre.name == name or name in genre.aliases:
                return genre

    def add_genre(self, new_genre: Genre) -> None:
        self.genres.append(new_genre)
        self.save_genres()

    def add_alias(self, alias: str, index: int = None, name: str = None):
        genre: Optional[Genre] = None
        if index is not None:
            genre = self.genres[index]
        elif name is not None:
            genre = self.find_genre(name)
        if genre is None:
            raise KeyError()
        genre.aliases.append(alias)
        self.save_genres()  # todo make sure it works (modifies self.genres)

    def save_genres(self):
        with open(f"db/data/genres.json", mode="w") as current_file:
            json.dumps([genre.to_dict() for genre in self.genres])
