import Database from 'better-sqlite3';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { DB_OPERATIONS } from '../enums/db';
import { CardSubRow, MinionCardRow } from '../constants/dbIpc';
import { executeQuery } from '../main/db';
import { buildDbQuery, SqlQuery } from '../main/dbQueries';

describe('database query execution', () => {
  it('passes SQL values as bound parameters and returns rows', () => {
    const rows = [{ id: 7 }];
    const all = jest.fn().mockReturnValue(rows);
    const prepare = jest.fn().mockReturnValue({ all });
    const database = { prepare } as unknown as Pick<
      Database.Database,
      'prepare'
    >;
    const query: SqlQuery = {
      statement: 'select id from minions where id = ?',
      params: [7],
    };

    expect(executeQuery(database, query)).toBe(rows);
    expect(prepare).toHaveBeenCalledWith(query.statement);
    expect(all).toHaveBeenCalledWith(7);
  });

  it('matches nested card filters and returns consistent list and count results', () => {
    const database = new Database(':memory:');
    database.exec(
      readFileSync(
        resolve(__dirname, '../../data/migrations/001_initial.sql'),
        'utf8',
      ),
    );
    database.exec(
      readFileSync(
        resolve(__dirname, '../../data/fixtures/representative.sql'),
        'utf8',
      ),
    );
    database.exec(`
      insert into episodes (id, season, episode, name, aliases, done)
      values (2, 2, 2, 'Second episode', '', 0);
      insert into scenes (id, episode, name, cards_done, all_characters_done, length)
      values (2, 2, 'Second scene', '', 0, 1);
      insert into cards
        (id, name, card_type, category, parent, nest_level, detailing_done)
      values
        (2, 'Second card', 'fixture', 'Fixture', 1, 0, 0),
        (3, 'Third card', 'fixture', 'Fixture', null, 0, 0),
        (4, 'Fourth card', 'fixture', 'Fixture', 2, 0, 0),
        (5, 'Fifth card', 'fixture', 'Fixture', 4, 0, 0);
      insert into minions
        (id, url, episode, scene, card_relations, all_characters_done, all_details_done, comments)
      values
        (2, 'second-image.png', 1, 1, '', 0, '', ''),
        (3, 'third-image.png', 2, 2, '', 0, '', '');
      insert into minion_card_relations
        (minion_id, card_id, rel, scene_id, episode_id)
      values
        (2, 1, 'fixture', 1, 1),
        (2, 2, 'fixture', 1, 1),
        (2, 2, 'duplicate', 1, 1),
        (3, 2, 'fixture', 2, 2),
        (3, 3, 'fixture', 2, 2),
        (3, 4, 'fixture', 2, 2),
        (3, 5, 'fixture', 2, 2);
    `);

    const query = {
      filter: {
        logic: 'all' as const,
        cards: { allOf: [1, 2], noneOf: [3] },
        seasons: { oneOf: [1] },
        views: [
          {
            logic: 'any' as const,
            episodes: { oneOf: [1] },
            scenes: { oneOf: [2] },
          },
        ],
      },
    };
    const rows = executeQuery(
      database,
      buildDbQuery({ operation: DB_OPERATIONS.GET_MINIONS, query }),
    );
    const countRows = executeQuery(
      database,
      buildDbQuery({ operation: DB_OPERATIONS.GET_MINIONS_COUNT, query }),
    ) as { total: number }[];

    expect(rows).toEqual([
      {
        id: 2,
        url: 'second-image.png',
        episode: 1,
        scene: 1,
        season: 1,
      },
    ]);
    expect(countRows[0].total).toBe(rows.length);

    const relatedCards = executeQuery(
      database,
      buildDbQuery({
        operation: DB_OPERATIONS.GET_MINION_CARDS,
        minionId: 3,
      }),
    ) as MinionCardRow[];
    expect(
      Object.fromEntries(
        relatedCards.map(({ id, isSelected }) => [id, isSelected]),
      ),
    ).toEqual({ 1: 0, 2: 1, 3: 1, 4: 1, 5: 1 });
    expect(relatedCards.filter(({ isSelected }) => isSelected).length).toBe(4);

    const updatedFilter = { logic: 'any' as const, scenes: { oneOf: [2] } };
    const update = buildDbQuery({
      operation: DB_OPERATIONS.UPDATE_CARD_FILTER,
      cardId: 1,
      filter: updatedFilter,
    });
    const updateResult = database
      .prepare(update.statement)
      .run(...update.params);
    expect(updateResult.changes).toBe(1);
    expect(
      (
        database.prepare('select view from cards where id = 1').get() as {
          view: string;
        }
      ).view,
    ).toBe(JSON.stringify(updatedFilter));
    database.close();
  });

  it('reports tag subtree counts and applies guarded card mutations', () => {
    const database = new Database(':memory:');
    database.exec(
      readFileSync(
        resolve(__dirname, '../../data/migrations/001_initial.sql'),
        'utf8',
      ),
    );
    database.exec(
      readFileSync(
        resolve(__dirname, '../../data/fixtures/representative.sql'),
        'utf8',
      ),
    );
    database.exec(`
      insert into cards
        (id, name, card_type, category, parent, nest_level, detailing_done)
      values
        (10, 'Root tag', 'tag', 'Tags', null, 0, 0),
        (11, 'Alpha sub', 'tag', 'Tags', 10, 1, 0),
        (12, 'Beta sub', 'tag', 'Tags', 10, 1, 0),
        (13, 'Deep sub', 'tag', 'Tags', 11, 2, 0);
      insert into minions
        (id, url, episode, scene, card_relations, all_characters_done, all_details_done, comments)
      values
        (2, 'second-image.png', 1, 1, '', 0, '', ''),
        (3, 'third-image.png', 1, 1, '', 0, '', '');
      insert into minion_card_relations
        (minion_id, card_id, rel, scene_id, episode_id)
      values
        (2, 10, 'p', 1, 1),
        (2, 11, 'p', 1, 1),
        (3, 13, 'p', 1, 1),
        (3, 12, 'x', 1, 1);
    `);

    const subs = executeQuery(
      database,
      buildDbQuery({ operation: DB_OPERATIONS.GET_CARD_SUBS, cardId: 10 }),
    ) as CardSubRow[];

    expect(
      subs.map(({ id, total, subtreeTotal }) => ({ id, total, subtreeTotal })),
    ).toEqual([
      { id: 11, total: 1, subtreeTotal: 2 },
      { id: 12, total: 0, subtreeTotal: 0 },
      { id: 13, total: 1, subtreeTotal: 1 },
      { id: 10, total: 1, subtreeTotal: 2 },
    ]);

    const runMutation = (request: Parameters<typeof buildDbQuery>[0]) => {
      const query = buildDbQuery(request);
      return database.prepare(query.statement).run(...query.params);
    };

    expect(
      runMutation({
        operation: DB_OPERATIONS.CREATE_CARD,
        parentId: 12,
        name: 'Created sub',
      }).changes,
    ).toBe(1);
    expect(
      database
        .prepare(
          'select name, card_type, category, parent, nest_level from cards where parent = 12',
        )
        .get(),
    ).toEqual({
      name: 'Created sub',
      card_type: 'tag',
      category: 'Tags',
      parent: 12,
      nest_level: 2,
    });

    expect(
      runMutation({
        operation: DB_OPERATIONS.RENAME_CARD,
        cardId: 12,
        name: 'Renamed sub',
      }).changes,
    ).toBe(1);
    expect(
      database.prepare('select name from cards where id = 12').get(),
    ).toEqual({ name: 'Renamed sub' });

    // A tag with subs, and a tag with relations, must both survive deletion.
    expect(
      runMutation({ operation: DB_OPERATIONS.DELETE_CARD, cardId: 12 }).changes,
    ).toBe(0);
    expect(
      runMutation({ operation: DB_OPERATIONS.DELETE_CARD, cardId: 13 }).changes,
    ).toBe(0);

    const created = database
      .prepare('select id from cards where name = ?')
      .get('Created sub') as { id: number };
    expect(
      runMutation({ operation: DB_OPERATIONS.DELETE_CARD, cardId: created.id })
        .changes,
    ).toBe(1);
    database.close();
  });
});
