rating_registry = {
    0: 0,
    13: 1,
    1: 2,
    54: 3,
    64: 4,
    118: 5,
    128: 6,
    186: 7,
    196: 8,
    242: 9,
    255: 10
}
reverse_rating_registry = {value: key for (key, value) in rating_registry.items()}


class RatingMapper:
    @staticmethod
    def from_mp3_tags(rating):
        return rating_registry.get(rating, -1)

    @staticmethod
    def to_mp3_tags(rating):
        return reverse_rating_registry.get(rating, 0)
