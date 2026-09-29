import createDbHandlers from '../main/dbHandlers';
import { DB_OPERATIONS } from '../enums/db';

describe('database IPC handlers', () => {
  const sender = {};
  const run = jest.fn();
  const viewExists = jest.fn();
  const trusted = jest.fn((event) => event === sender);
  const handlers = createDbHandlers(run, trusted, viewExists);

  beforeEach(() => {
    jest.clearAllMocks();
    run.mockReturnValue([]);
    viewExists.mockReturnValue(false);
  });

  it('does not call the database for untrusted senders', () => {
    expect(handlers.labels({})).toEqual({
      ok: false,
      error: { code: 'UNAVAILABLE', message: 'Request unavailable.' },
    });
    expect(run).not.toHaveBeenCalled();
  });

  it('allow-lists category kinds and never accepts an operation number', () => {
    expect(handlers.categories(sender, 'tags')).toEqual({ ok: true, data: [] });
    expect(run).toHaveBeenCalledWith({
      operation: DB_OPERATIONS.GET_TAG_CATEGORIES,
    });
    run.mockClear();
    expect(handlers.categories(sender, -1)).toMatchObject({
      ok: false,
      error: { code: 'INVALID_REQUEST' },
    });
    expect(run).not.toHaveBeenCalled();
  });

  it('rejects malformed IDs, pages, and unexpected query fields', () => {
    expect(handlers.cards(sender, ['1; DROP TABLE cards'])).toMatchObject({
      ok: false,
      error: { code: 'INVALID_REQUEST' },
    });
    expect(handlers.minions(sender, {}, -1)).toMatchObject({
      ok: false,
      error: { code: 'INVALID_REQUEST' },
    });
    expect(
      handlers.minions(sender, { table: 'sqlite_master' }, 0),
    ).toMatchObject({
      ok: false,
      error: { code: 'INVALID_REQUEST' },
    });
    expect(
      handlers.minions(sender, { cards: [1], rel: "p' OR 1=1" }, 0),
    ).toMatchObject({
      ok: false,
      error: { code: 'INVALID_REQUEST' },
    });
    expect(run).not.toHaveBeenCalled();
  });

  it('rejects unknown views and accepts only existing, well-formed view names', () => {
    expect(handlers.minions(sender, { view: 'other;DROP' }, 0)).toMatchObject({
      ok: false,
      error: { code: 'INVALID_REQUEST' },
    });
    expect(handlers.minions(sender, { view: 'private_view' }, 0)).toMatchObject(
      {
        ok: false,
        error: { code: 'INVALID_REQUEST' },
      },
    );
    viewExists.mockReturnValue(true);
    expect(handlers.minions(sender, { view: 'public_view' }, 0)).toEqual({
      ok: true,
      data: [],
    });
    expect(run).toHaveBeenCalledWith({
      operation: DB_OPERATIONS.GET_MINIONS,
      query: { view: 'public_view' },
      page: 0,
    });
  });

  it('returns structured failures rather than hiding database errors as empty rows', () => {
    run.mockImplementation(() => {
      throw new Error('sensitive database details');
    });
    expect(handlers.labels(sender)).toEqual({
      ok: false,
      error: { code: 'DATABASE_ERROR', message: 'Could not load data.' },
    });
  });

  it('returns validated count values', () => {
    run.mockReturnValue([{ total: 12 }]);
    expect(handlers.minionCount(sender, { episodes: [1] })).toEqual({
      ok: true,
      data: 12,
    });
    expect(handlers.minionCount(sender, { episodes: [1.5] })).toMatchObject({
      ok: false,
      error: { code: 'INVALID_REQUEST' },
    });
  });

  it('accepts validated season filters', () => {
    expect(handlers.minions(sender, { seasons: [1, 3] }, 0)).toEqual({
      ok: true,
      data: [],
    });
    expect(run).toHaveBeenCalledWith({
      operation: DB_OPERATIONS.GET_MINIONS,
      query: { seasons: [1, 3] },
      page: 0,
    });
    expect(handlers.minions(sender, { seasons: [1.5] }, 0)).toMatchObject({
      ok: false,
      error: { code: 'INVALID_REQUEST' },
    });
  });

  it('validates nested filter shapes and accepts supported conditions', () => {
    const filter = {
      logic: 'all',
      cards: { oneOf: [1, 2], noneOf: [4] },
      views: [{ logic: 'any', scenes: { allOf: [5] } }],
    };
    expect(handlers.minions(sender, { filter }, 0)).toEqual({
      ok: true,
      data: [],
    });
    expect(run).toHaveBeenCalledWith({
      operation: DB_OPERATIONS.GET_MINIONS,
      query: { filter },
      page: 0,
    });
    expect(
      handlers.minions(
        sender,
        { filter: { logic: 'xor', cards: { oneOf: [1] } } },
        0,
      ),
    ).toMatchObject({ ok: false, error: { code: 'INVALID_REQUEST' } });
    expect(
      handlers.minions(
        sender,
        { filter: { logic: 'all', cards: { oneOf: [] } } },
        0,
      ),
    ).toMatchObject({ ok: false, error: { code: 'INVALID_REQUEST' } });
  });

  it('accepts only boolean random-order options', () => {
    expect(handlers.minions(sender, { cards: [1], random: true }, 0)).toEqual({
      ok: true,
      data: [],
    });
    expect(
      handlers.minions(sender, { cards: [1], random: 'yes' }, 0),
    ).toMatchObject({ ok: false, error: { code: 'INVALID_REQUEST' } });
  });

  it('validates and dispatches card filter updates', () => {
    run.mockReturnValue({ changes: 1 });
    const filter = { logic: 'all', cards: { oneOf: [1] } };
    expect(handlers.updateCardFilter(sender, 9, filter)).toEqual({
      ok: true,
      data: true,
    });
    expect(run).toHaveBeenCalledWith({
      operation: DB_OPERATIONS.UPDATE_CARD_FILTER,
      cardId: 9,
      filter,
    });
    expect(handlers.updateCardFilter(sender, -1, filter)).toMatchObject({
      ok: false,
      error: { code: 'INVALID_REQUEST' },
    });
  });

  it('validates and dispatches related-card queries', () => {
    expect(handlers.minionCards(sender, 42)).toEqual({ ok: true, data: [] });
    expect(run).toHaveBeenCalledWith({
      operation: DB_OPERATIONS.GET_MINION_CARDS,
      minionId: 42,
    });
    expect(handlers.minionCards(sender, -1)).toMatchObject({
      ok: false,
      error: { code: 'INVALID_REQUEST' },
    });
  });
});
