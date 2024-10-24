import unittest

from functions.data_types.ArtistRole import ArtistRole
from functions.execute.parse.args_parsing_errors import ArgsParsingError
from functions.execute.parse.parse_args import parse_args
from functions.file_import.read_file import predicted_artists_and_title
from libs.error_handling import error_message_to_string

ORIGINAL = [ArtistRole.Original]
ORIGINAL_FEAT = [ArtistRole.Original, ArtistRole.Feat]
REMIXER = [ArtistRole.Remixer]
REMIXER_FEAT = [ArtistRole.Remixer, ArtistRole.Feat]


class Test(unittest.TestCase):

    def test_should_parse_one_artist_and_title(self):
        file_name = "Blaynoise - Venom Eve"
        title, artists = predicted_artists_and_title(file_name)
        self.assertEqual(title, "Venom Eve")
        self.assertDictEqual(artists, {"Blaynoise": ORIGINAL})

    def test_should_parse_two_artists_and_title(self):
        file_name = "Blaynoise & Budzy - Venom Eve"
        title, artists = predicted_artists_and_title(file_name)
        self.assertEqual(title, "Venom Eve")
        self.assertDictEqual(artists, {"Blaynoise": ORIGINAL, "Budzy": ORIGINAL})

    def test_should_parse_one_artists_plus_feat_and_title(self):
        file_name = "Blaynoise feat. Budzy - Venom Eve"
        title, artists = predicted_artists_and_title(file_name)
        self.assertEqual(title, "Venom Eve")
        self.assertDictEqual(artists, {"Blaynoise": ORIGINAL, "Budzy": ORIGINAL_FEAT})

    def test_should_parse_one_remixer_and_one_original_and_title(self):
        file_name = "Budzy - Venom Eve [Blaynoise]"
        title, artists = predicted_artists_and_title(file_name)
        self.assertEqual(title, "Venom Eve")
        self.assertDictEqual(artists, {"Blaynoise": ORIGINAL, "Budzy": REMIXER})

    def test_should_parse_complex_example(self):
        file_name = (
            "Budzy & Aviators feat. Datphoria, Blue Brony & Alex S. - Venom Eve & Whatever (Long Mix)"
            " [Blaynoise, Zynthia & Spag Heddy feat. Lena del Rey]"
        )
        title, artists = predicted_artists_and_title(file_name)
        self.assertEqual(title, "Venom Eve & Whatever (Long Mix)")
        self.assertDictEqual(
            artists,
            {
                "Blaynoise": ORIGINAL,
                "Zynthia": ORIGINAL,
                "Spag Heddy": ORIGINAL,
                "Lena del Rey": ORIGINAL_FEAT,
                "Budzy": REMIXER,
                "Aviators": REMIXER,
                "Datphoria": REMIXER_FEAT,
                "Blue Brony": REMIXER_FEAT,
                "Alex S.": REMIXER_FEAT,
            },
        )
