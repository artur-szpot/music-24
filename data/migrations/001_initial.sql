-- Version 1 baseline from the supplied SQLite definitions.
-- Apply only to a new, empty SQLite database. Never apply to an existing collection.
BEGIN;

CREATE TABLE "episodes" (
  "id" INTEGER NOT NULL,
  "season" INTEGER NOT NULL,
  "episode" INTEGER NOT NULL,
  "name" TEXT NOT NULL,
  "aliases" TEXT NOT NULL,
  "done" INTEGER NOT NULL,
  PRIMARY KEY("id")
);

CREATE TABLE "scenes" (
  "id" INTEGER NOT NULL,
  "episode" INTEGER NOT NULL,
  "name" TEXT NOT NULL,
  "cards_done" TEXT NOT NULL,
  "all_characters_done" INTEGER NOT NULL,
  "length" INTEGER NOT NULL,
  PRIMARY KEY("id")
);

CREATE TABLE "minions" (
  "id" INTEGER NOT NULL,
  "url" TEXT NOT NULL,
  "episode" INTEGER NOT NULL,
  "scene" INTEGER NOT NULL,
  "card_relations" TEXT NOT NULL,
  "all_characters_done" INTEGER NOT NULL,
  "all_details_done" TEXT NOT NULL,
  "comments" TEXT NOT NULL,
  PRIMARY KEY("id")
);

CREATE TABLE "scene_cards_done" (
  "scene_id" INTEGER NOT NULL,
  "card_id" INTEGER NOT NULL
);

CREATE TABLE "minion_card_relations" (
  "minion_id" INTEGER NOT NULL,
  "card_id" INTEGER NOT NULL,
  "rel" TEXT NOT NULL,
  "scene_id" INTEGER NOT NULL,
  "episode_id" INTEGER NOT NULL
);

CREATE TABLE "dominion_card_relations" (
  "main_card_id" INTEGER NOT NULL,
  "related_card_id" INTEGER NOT NULL
);

CREATE TABLE "minion_cards" (
  "id" INTEGER NOT NULL,
  "card_id" INTEGER NOT NULL,
  "minion_id" INTEGER NOT NULL,
  "is_3d" INTEGER NOT NULL DEFAULT 0,
  "can_be_3d" INTEGER NOT NULL DEFAULT 0,
  "edit_needed" TEXT,
  "is_reserve" INTEGER DEFAULT 0,
  PRIMARY KEY("id" AUTOINCREMENT),
  FOREIGN KEY("minion_id") REFERENCES "minion_cards"("id")
);

CREATE TABLE "dominion_card_sets" (
  "id" INTEGER NOT NULL,
  "name" TEXT NOT NULL,
  "pony_name" TEXT,
  "pony_description" TEXT,
  PRIMARY KEY("id")
);

CREATE TABLE "dominion_cards" (
  "id" INTEGER NOT NULL,
  "set" INTEGER NOT NULL,
  "name" TEXT NOT NULL,
  "total" INTEGER NOT NULL,
  "kingdom" INTEGER NOT NULL DEFAULT 1,
  "pony_name" TEXT,
  PRIMARY KEY("id"),
  FOREIGN KEY("set") REFERENCES "dominion_card_sets"("id")
);

CREATE VIEW minion_card_relations_counts AS
SELECT card_id, rel, count(1) AS total
FROM minion_card_relations
GROUP BY card_id, rel;

CREATE TABLE "cards" (
  "id" INTEGER NOT NULL,
  "name" TEXT NOT NULL,
  "card_type" TEXT NOT NULL,
  "category" TEXT,
  "parent" INTEGER,
  "last_visited_scene" INTEGER,
  "nest_level" INTEGER NOT NULL,
  "subs_done" TEXT,
  "detailing_done" INTEGER NOT NULL,
  "filters" TEXT,
  "original" INTEGER,
  "view" TEXT,
  PRIMARY KEY("id")
);

CREATE VIEW minion_episodes_counts AS
SELECT episode, count(1) AS total FROM minions GROUP BY episode;

CREATE VIEW minion_scenes_counts AS
SELECT scene, count(1) AS total FROM minions GROUP BY scene;

CREATE TABLE "representatives" (
  "id" INTEGER NOT NULL,
  "category" TEXT NOT NULL,
  "minion_id" INTEGER NOT NULL
);

PRAGMA user_version = 1;
COMMIT;
