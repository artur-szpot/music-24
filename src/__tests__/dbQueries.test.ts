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
        scenes: [6],
      },
      page: 2,
    });

    expect(query.statement).not.toContain("p' OR 1=1 --");
    expect(query.statement).toContain('mcr.card_id in (?, ?)');
    expect(query.statement).toContain('and rel = ?');
    expect(query.statement).toContain('limit ? offset ?');
    expect(query.params).toEqual([3, 8, "p' OR 1=1 --", 12, 4, 6, 12, 24]);
  });

  it('binds card IDs and pagination in count queries', () => {
    const query = buildDbQuery({
      operation: DB_OPERATIONS.GET_MINIONS_COUNT,
      query: { cards: [2, 5], rel: 'parent' },
      page: 3,
    });

    expect(query.statement).toContain('mcr.card_id in (?, ?)');
    expect(query.statement).toContain('and rel = ?');
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
