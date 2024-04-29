class MusicFile:
    authors = []
    genres = []
    title = ""
    path = ""
    length = 0
    rating = 0
    is_mlp = False
    is_dad = False
    is_ready = False

    def __init__(self, authors, genres) -> None:
        self.authors = authors
        self.genres = genres
