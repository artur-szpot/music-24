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
    errors = []

    def __init__(self, source) -> None:
        self.authors = source.get('authors')
        self.genres = source.get('genres')
        self.title = source.get('title')
        self.path = source.get('path')
        self.length = source.get('length')
        self.rating = source.get('rating')
        self.is_mlp = source.get('is_mlp')
        self.is_dad = source.get('is_dad')
        self.is_ready = source.get('is_ready')
        self.errors = source.get('errors')

    def to_dict(self):
        return {
            'authors': self.authors,
            'genres': self.genres,
            'title': self.title,
            'path': self.path,
            'length': self.length,
            'rating': self.rating,
            'is_mlp': self.is_mlp,
            'is_dad': self.is_dad,
            'is_ready': self.is_ready,
        }
