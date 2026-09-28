# Data contract

`migrations/001_initial.sql` captures the supplied SQLite schema as version 1.
It creates tables and views in a **new, empty** database and sets SQLite's
`PRAGMA user_version` to 1. The application has no migration runner and does
not apply this SQL on startup. Neither the schema nor the fixture belongs in a
production database.

The numbered SQL files are the historical contract: do not rewrite version 1
when columns or domain values evolve. Add a new, numbered migration for each
future change, describing upgrade steps, compatibility, and how existing data
is preserved. An existing collection may have different tables, columns, or
user_version; compare its schema with this baseline and back it up before
planning an upgrade. Do **not** stamp an existing database with version 1
without verifying its schema. There is currently no automated compatibility
check or supported upgrade path for existing collections.

`fixtures/representative.sql` contains only invented records for tests on a
disposable database. It is not an import workflow, a production seed, or a
launchable image collection. The invented card type, relation, and filename
are not assertions about permitted production values. It contains no images.

## Schema notes

The baseline includes `episodes`, `scenes`, `minions`, `cards`,
`scene_cards_done`, `minion_card_relations`, `minion_cards`,
`dominion_card_sets`, `dominion_cards`, `dominion_card_relations`, and
`representatives`, plus the three count views
`minion_card_relations_counts`, `minion_episodes_counts`, and
`minion_scenes_counts`. Column types, nullability, defaults, and declared
foreign keys are in the migration; SQLite creates `sqlite_sequence` for the
`AUTOINCREMENT` table automatically.

The supplied `minion_cards.minion_id` foreign key references
`minion_cards(id)` rather than `minions(id)`. This is preserved in version 1;
correcting it requires assessing existing data and writing a later migration.
`src/main/db.ts` currently selects a `filter` column from `minions` in
`GET_MINION`, but that column is absent from the supplied schema. That query
may fail with this baseline; it is not evidence that a `filter` column exists
in production.

## Image roots and naming

Runtime configuration requests a database file and three separate image roots:
`minionRoot`, `cardRoot`, and `fileSystemRoot`. The main process registers
`minion`, `card`, and `file-system` protocols against those roots respectively.
It resolves each requested URL pathname under its root and rejects paths that
escape the root.

The renderer's `Minion` component builds an image URL as
`minion:///<episode>/<minions.url>`. For example, an episode value of `1` and
URL value of `fixture-image.png` request a path under the minion root at
`1/fixture-image.png`; that example describes URL construction, **not** an
existing image or a required filename format. The schema stores `minions.url`
as text but imposes no naming convention or file extension. No card or general
file-system image filename convention is established by the supplied schema
or current renderer code. An existing collection must supply files consistent
with the URLs that the application actually requests; none are distributed
here.
