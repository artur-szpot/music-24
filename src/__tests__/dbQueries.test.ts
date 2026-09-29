import { DB_OPERATIONS } from '../enums/db';
import { buildDbQuery } from '../main/dbQueries';

describe('database query construction', () => {
  it('binds filters, relationship values, and pagination in SQL order', () => {
    const query = buildDbQuery({
      operation: DB_OPERATIONS.GET_MINIONS,
      query: {
        cards: [3, 8],
        rel: "p' OR 1=1 --",
        ids: [12],
        episodes: [4],
        seasons: [2],
        scenes: [6],
      },
      page: 2,
    });

    expect(query.statement).not.toContain("p' OR 1=1 --");
    expect(query.statement).toContain('mcr.card_id in (?, ?)');
    expect(query.statement).toContain('and mcr.rel = ?');
    expect(query.statement).toContain('limit ? offset ?');
    expect(query.params).toEqual([12, 4, 2, 6, 3, 8, "p' OR 1=1 --", 12, 24]);
  });

  it('binds card IDs and pagination in count queries', () => {
    const query = buildDbQuery({
      operation: DB_OPERATIONS.GET_MINIONS_COUNT,
      query: { cards: [2, 5], rel: 'parent' },
      page: 3,
    });

    expect(query.statement).toContain('mcr.card_id in (?, ?)');
    expect(query.statement).toContain('and mcr.rel = ?');
    expect(query.statement).toContain('limit ? offset ?');
    expect(query.params).toEqual([2, 5, 'parent', 12, 36]);
  });

  it('binds IDs in card lookup queries', () => {
    const query = buildDbQuery({
      operation: DB_OPERATIONS.GET_CARDS,
      query: { ids: [1, 9] },
    });

    expect(query.statement).toContain('where id in (?, ?)');
    expect(query.params).toEqual([1, 9]);
  });

  it('filters minions by season through their episode records', () => {
    const query = buildDbQuery({
      operation: DB_OPERATIONS.GET_MINIONS,
      query: { seasons: [1, 3] },
    });

    expect(query.statement).toContain(
      'm.episode in (select id from episodes where season in (?, ?))',
    );
    expect(query.statement).toContain(
      'select season from episodes e where e.id = m.episode',
    );
    expect(query.params).toEqual([1, 3, 12, 0]);
  });

  it('builds nested any/all filters with bound values', () => {
    const query = buildDbQuery({
      operation: DB_OPERATIONS.GET_MINIONS,
      query: {
        filter: {
          logic: 'all',
          cards: { oneOf: [2, 3], allOf: [5], noneOf: [7] },
          seasons: { oneOf: [1, 4] },
          views: [{ logic: 'any', scenes: { oneOf: [8, 9] } }],
        },
      },
    });

    expect(query.statement).toContain('mcr.card_id in (?, ?)');
    expect(query.statement).toContain('count(distinct mcr.card_id)');
    expect(query.statement).toContain('not exists');
    expect(query.statement).toContain('where season in (?, ?)');
    expect(query.statement).toContain('m.scene in (?, ?)');
    expect(query.params).toEqual([2, 3, 5, 7, 1, 4, 8, 9, 12, 0]);
  });

  it('keeps allOf membership grouped when its parent logic is any', () => {
    const query = buildDbQuery({
      operation: DB_OPERATIONS.GET_MINIONS,
      query: {
        filter: {
          logic: 'any',
          episodes: { allOf: [2, 4] },
          scenes: { oneOf: [9] },
        },
      },
    });

    expect(query.statement).toContain('(m.episode = ? and m.episode = ?)');
    expect(query.statement).toContain(
      '(((m.episode = ? and m.episode = ?)) or (m.scene in (?)))',
    );
    expect(query.params).toEqual([2, 4, 9, 12, 0]);
  });

  it('randomizes related-minion results for representative selection', () => {
    const query = buildDbQuery({
      operation: DB_OPERATIONS.GET_MINIONS,
      query: { cards: [4], random: true },
    });

    expect(query.statement).toContain('order by random()');
    expect(query.params).toEqual([4, 12, 0]);
  });

  it('binds serialized filter edits and card IDs in update queries', () => {
    const filter = { logic: 'all' as const, cards: { oneOf: [4] } };
    const query = buildDbQuery({
      operation: DB_OPERATIONS.UPDATE_CARD_FILTER,
      cardId: 9,
      filter,
    });

    expect(query.statement).toBe('update cards set view = ? where id = ?');
    expect(query.params).toEqual([JSON.stringify(filter), 9]);
  });

  it('binds minion IDs for related-card hierarchy queries', () => {
    const query = buildDbQuery({
      operation: DB_OPERATIONS.GET_MINION_CARDS,
      minionId: 42,
    });

    expect(query.statement).toContain('with recursive selected_cards');
    expect(query.statement).toContain('parent_card.id = child.parent');
    expect(query.params).toEqual([42]);
  });

  it('accepts only explicitly allow-listed view identifiers', () => {
    expect(() =>
      buildDbQuery({
        operation: DB_OPERATIONS.GET_MINIONS,
        query: { view: 'minions' },
      }),
    ).toThrow('Unknown database view.');
    expect(() =>
      buildDbQuery(
        {
          operation: DB_OPERATIONS.GET_MINIONS,
          query: { view: 'minions; drop_table' },
        },
        ['minions; drop_table'],
      ),
    ).toThrow('Unknown database view.');

    const query = buildDbQuery(
      {
        operation: DB_OPERATIONS.GET_MINIONS,
        query: { view: 'public_minions' },
      },
      ['public_minions'],
    );
    expect(query.statement).toContain('from public_minions');
    expect(query.params).toEqual([12, 0]);
  });
});
