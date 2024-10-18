from enum import Enum


class IgnoreFilenameDifferences(Enum):
    CONSISTENT_FILENAME = "consistent_filename"
    MISMATCHED_ARTISTS = "mismatched_artists"
    ARTISTS_MISSING_FROM_TAGS = "artists_missing_from_tags"
    ARTISTS_MISSING_FROM_FILENAME = "artists_missing_from_filename"
    CONSISTENT_TITLE = "consistent_title"
