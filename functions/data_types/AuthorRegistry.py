import json
from typing import Optional, List

from functions.data_types.Author import Author


class AuthorRegistry:
    authors: List[Author]

    def __init__(self):
        try:
            with open(f"db/data/authors.json", mode="r") as current_file:
                self.authors = [
                    Author.from_dict(value) for value in json.loads(current_file.read())
                ]
        except:
            self.authors = []

    def find_author(self, name: str) -> Optional[Author]:
        for author in self.authors:
            if author.name == name or name in author.aliases:
                return author

    def add_author(self, new_author: Author) -> None:
        self.authors.append(new_author)
        self.save_authors()

    def add_alias(self, alias: str, index: int = None, name: str = None):
        author: Optional[Author] = None
        if index is not None:
            author = self.authors[index]
        elif name is not None:
            author = self.find_author(name)
        if author is None:
            raise KeyError()
        author.aliases.append(alias)
        self.save_authors()  # todo make sure it works (modifies self.authors)

    def save_authors(self):
        with open(f"db/data/authors.json", mode="w") as current_file:
            json.dumps([author.to_dict() for author in self.authors])
