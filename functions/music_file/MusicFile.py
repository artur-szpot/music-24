from typing import List, Dict, Any, Optional

from functions.data_types.ArtistRole import ArtistRole
from functions.music_file.IgnoreFilenameDifferences import IgnoreFilenameDifferences
from functions.music_file.MusicFileDbProps import MusicFileDbProps
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileViewProps import MusicFileViewProps


class MusicFile:
    artists: Dict[str, List[ArtistRole]]
    genres: List[str]
    title: Optional[str]
    path: str
    db_file: Optional[str]
    filename: Optional[str]
    length: Optional[int]
    rating: Optional[int]
    is_mlp: Optional[bool]
    is_dad: Optional[bool]
    is_ready: Optional[bool]

    predicted_artists: Optional[Dict[str, List[ArtistRole]]]
    predicted_title: Optional[str]
    ignore_predicted_filename_differences: Dict[IgnoreFilenameDifferences, bool]

    errors: List[MusicFileError]
    warnings: List[MusicFileError]

    db_props: Dict[MusicFileDbProps, Any]
    view_props: Dict[MusicFileViewProps, Any]

    def __init__(
        self,
        artists: Dict[str, List[ArtistRole]],
        genres: List[str],
        title: Optional[str],
        path: str,
        db_file: Optional[str],
        filename: Optional[str],
        length: Optional[int],
        rating: Optional[int],
        is_mlp: Optional[bool],
        is_dad: Optional[bool],
        is_ready: Optional[bool],
        predicted_artists: Optional[Dict[str, List[ArtistRole]]] = None,
        predicted_title: Optional[str] = None,
        ignore_predicted_filename_differences: Dict[
            IgnoreFilenameDifferences, bool
        ] = None,
        errors: List[MusicFileError] = None,
        warnings: List[MusicFileError] = None,
        db_props: Dict[MusicFileDbProps, Any] = None,
        view_props: Dict[MusicFileViewProps, Any] = None,
    ) -> None:
        self.artists = artists
        self.genres = genres
        self.title = title
        self.path = path
        self.filename = filename
        self.db_file = db_file
        self.length = length
        self.rating = rating
        self.is_mlp = is_mlp
        self.is_dad = is_dad
        self.is_ready = is_ready
        self.errors = errors or []
        self.warnings = warnings or []
        self.predicted_artists = predicted_artists or []
        self.predicted_title = predicted_title
        self.db_props = db_props or {}
        self.view_props = view_props or {}
        self.ignore_predicted_filename_differences = (
            ignore_predicted_filename_differences
            or {key: False for key in IgnoreFilenameDifferences}
        )

    @staticmethod
    def from_dict(source):
        return MusicFile(
            artists=source.get("artists", {}),
            genres=source.get("genres", []),
            title=source.get("title"),
            path=source.get("path"),
            filename=source.get("filename"),
            db_file=source.get("db_file"),
            length=source.get("length"),
            rating=source.get("rating"),
            is_mlp=source.get("is_mlp"),
            is_dad=source.get("is_dad"),
            is_ready=source.get("is_ready"),
            errors=source.get("errors", []),
            warnings=source.get("warnings", []),
            predicted_artists=source.get("predicted_artists", []),
            predicted_title=source.get("predicted_title", ""),
            db_props=source.get("db_props", {}),
            view_props=source.get("view_props", {}),
            ignore_predicted_filename_differences={
                key: False for key in IgnoreFilenameDifferences
            },
        )

    def to_dict(self):
        return {
            "artists": self.artists,
            "artists_string": ", ".join(artist for artist in self.artists),
            "genres": self.genres,
            "title": self.title,
            "path": self.path,
            "filename": self.filename,
            "db_file": self.db_file,
            "length": self.length,
            "rating": self.rating,
            "is_mlp": self.is_mlp,
            "is_dad": self.is_dad,
            "is_ready": self.is_ready,
        }

    def set_db_prop(self, prop, value: Any) -> None:
        self.db_props[prop] = value

    def get_db_prop(self, prop: MusicFileDbProps) -> Any:
        return self.db_props.get(prop)

    def set_view_props(self, ordinal_number: int, highlighted: bool = False) -> None:
        self.view_props = {
            MusicFileViewProps.OrdinalNumber: ordinal_number + 1,
            MusicFileViewProps.Highlighted: highlighted,
        }

    def get_ordinal_number(self) -> int:
        return self.view_props.get(MusicFileViewProps.OrdinalNumber, 0)

    def get_highlighted(self) -> bool:
        return self.view_props.get(MusicFileViewProps.Highlighted, False)

    @staticmethod
    def create_artists_substring(artists: List[str]) -> str:
        if len(artists) == 1:
            artists_string = artists[0]
        else:
            if any(["&" in artist for artist in artists]):
                artists_string = ", ".join(artists)
            else:
                artists_string = f"{', '.join(artists[:-1])} & {artists[-1]}"
        return artists_string

    @staticmethod
    def create_artists_string(main: List[str], feat: List[str]) -> str:
        if not len(main):
            return ""
        artists_string = MusicFile.create_artists_substring(main)
        if len(feat):
            artists_string += f" feat. {MusicFile.create_artists_substring(feat)}"
        return artists_string

    def create_filename(self) -> str:
        main_artists = []
        main_feat_artists = []
        original_artists = []
        original_feat_artists = []
        for artist, roles in self.artists.items():
            original = ArtistRole.Original in roles
            feat = ArtistRole.Feat in roles
            if original:
                if feat:
                    main_feat_artists.append(artist)
                else:
                    main_artists.append(artist)
            else:
                if feat:
                    original_feat_artists.append(artist)
                else:
                    original_artists.append(artist)
        original_artists_string = MusicFile.create_artists_string(
            original_artists, original_feat_artists
        )
        title = f"{MusicFile.create_artists_string(main_artists, main_feat_artists)} - {self.title}"
        if original_artists_string:
            title += f" [{original_artists_string}]"
        return title
