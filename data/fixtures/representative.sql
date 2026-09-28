-- Synthetic data for a disposable test database created with 001_initial.sql.
-- Never run against a production database or an existing image collection.
-- Names, relation values, and image references are not a verified domain contract.
BEGIN;

INSERT INTO episodes (id, season, episode, name, aliases, done)
VALUES (1, 1, 1, 'Fixture episode', '', 0);

INSERT INTO scenes (id, episode, name, cards_done, all_characters_done, length)
VALUES (1, 1, 'Fixture scene', '', 0, 1);

INSERT INTO cards
  (id, name, card_type, category, parent, last_visited_scene,
   nest_level, subs_done, detailing_done, filters, original, "view")
VALUES
  (1, 'Fixture card', 'fixture', 'Fixture', NULL, NULL,
   0, NULL, 0, NULL, NULL, NULL);

INSERT INTO minions
  (id, url, episode, scene, card_relations, all_characters_done,
   all_details_done, comments)
VALUES
  (1, 'fixture-image.png', 1, 1, '', 0, '', '');

INSERT INTO scene_cards_done (scene_id, card_id) VALUES (1, 1);

INSERT INTO minion_card_relations
  (minion_id, card_id, rel, scene_id, episode_id)
VALUES (1, 1, 'fixture', 1, 1);

INSERT INTO representatives (id, category, minion_id)
VALUES (1, 'fixture', 1);

INSERT INTO dominion_card_sets (id, name, pony_name, pony_description)
VALUES (1, 'Fixture set', NULL, NULL);

INSERT INTO dominion_cards (id, "set", name, total, kingdom, pony_name)
VALUES (1, 1, 'Fixture dominion card', 0, 1, NULL);

INSERT INTO dominion_card_relations (main_card_id, related_card_id)
VALUES (1, 1);

-- Preserve the supplied self-referencing foreign key in the baseline.
INSERT INTO minion_cards (id, card_id, minion_id)
VALUES (1, 1, 1);

COMMIT;
