import {
  CardRow,
  CardSubRow,
  CategoryKind,
  CategoryRow,
  IpcErrorCode,
  IpcResult,
  LabelRow,
  MinionCardRow,
  MinionFilter,
  MinionQuery,
  MinionRow,
} from '../constants/dbIpc';
import { LIMITS } from '../constants/limits';
import { DB_OPERATIONS } from '../enums/db';

export type DbRequest =
  | {
      operation:
        | DB_OPERATIONS.INITIALIZE_LABELS
        | DB_OPERATIONS.GET_TAG_CATEGORIES
        | DB_OPERATIONS.GET_IMPLEMENTATION_CATEGORIES
        | DB_OPERATIONS.GET_EPISODES
        | DB_OPERATIONS.GET_SCENES;
    }
  | { operation: DB_OPERATIONS.GET_CARDS; query: { ids: number[] } }
  | {
      operation: DB_OPERATIONS.UPDATE_CARD_FILTER;
      cardId: number;
      filter: MinionFilter;
    }
  | { operation: DB_OPERATIONS.GET_MINION_CARDS; minionId: number }
  | { operation: DB_OPERATIONS.GET_CARD_SUBS; cardId: number }
  | { operation: DB_OPERATIONS.CREATE_CARD; parentId: number; name: string }
  | { operation: DB_OPERATIONS.RENAME_CARD; cardId: number; name: string }
  | { operation: DB_OPERATIONS.DELETE_CARD; cardId: number }
  | {
      operation: DB_OPERATIONS.GET_MINIONS | DB_OPERATIONS.GET_MINIONS_COUNT;
      query: MinionQuery;
      page?: number;
    };

type Runner = (request: DbRequest) => unknown;
type Guard = (event: unknown) => boolean;
type ViewChecker = (name: string) => boolean;

class RequestError extends Error {}

function invalid(message: string): never {
  throw new RequestError(message);
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function ids(value: unknown): number[] {
  if (
    !Array.isArray(value) ||
    !value.length ||
    value.length > LIMITS.MAX_QUERY_IDS ||
    !value.every((id) => Number.isSafeInteger(id) && id >= 0)
  ) {
    return invalid(
      `IDs must be a nonempty list of at most ${LIMITS.MAX_QUERY_IDS} nonnegative integers.`,
    );
  }
  return value;
}

function identifier(value: unknown, label: string): number {
  if (!Number.isSafeInteger(value) || (value as number) < 0) {
    return invalid(`${label} must be a nonnegative integer.`);
  }
  return value as number;
}

function cardName(value: unknown): string {
  const name = typeof value === 'string' ? value.trim() : '';
  if (
    !name ||
    name.length > LIMITS.MAX_CARD_NAME ||
    Array.from(name).some((character) => character.charCodeAt(0) < 32)
  ) {
    return invalid(
      `Card names must be 1 to ${LIMITS.MAX_CARD_NAME} printable characters.`,
    );
  }
  return name;
}

function changed(result: unknown): boolean {
  if (!isRecord(result) || !Number.isSafeInteger(result.changes)) {
    throw new Error('Unexpected database update result.');
  }
  return result.changes === 1;
}

function parseFilter(value: unknown): MinionFilter {
  let nodeCount = 0;
  let totalIds = 0;

  const parseNode = (node: unknown, depth: number): MinionFilter => {
    nodeCount += 1;
    if (
      depth > 8 ||
      nodeCount > 100 ||
      !isRecord(node) ||
      Object.keys(node).some(
        (key) =>
          ![
            'logic',
            'cards',
            'seasons',
            'episodes',
            'scenes',
            'views',
          ].includes(key),
      ) ||
      (node.logic !== 'any' && node.logic !== 'all')
    ) {
      return invalid('Invalid minion filter.');
    }

    const filter: MinionFilter = { logic: node.logic };
    let conditionCount = 0;
    (['cards', 'seasons', 'episodes', 'scenes'] as const).forEach((key) => {
      const rawCategory = node[key];
      if (rawCategory === undefined) return;
      if (
        !isRecord(rawCategory) ||
        Object.keys(rawCategory).some(
          (operator) => !['oneOf', 'allOf', 'noneOf'].includes(operator),
        )
      ) {
        return invalid('Invalid minion filter category.');
      }
      const category = {} as NonNullable<MinionFilter[typeof key]>;
      (['oneOf', 'allOf', 'noneOf'] as const).forEach((operator) => {
        if (rawCategory[operator] !== undefined) {
          const values = ids(rawCategory[operator]);
          totalIds += values.length;
          if (totalIds > 2000) {
            return invalid('Filters may contain at most 2000 IDs.');
          }
          category[operator] = [...new Set(values)];
          conditionCount += 1;
        }
      });
      if (!Object.keys(category).length) {
        return invalid('Filter categories must contain conditions.');
      }
      filter[key] = category;
    });

    if (node.views !== undefined) {
      if (
        !Array.isArray(node.views) ||
        !node.views.length ||
        node.views.length > 100
      ) {
        return invalid('Invalid nested minion filters.');
      }
      filter.views = node.views.map((child) => parseNode(child, depth + 1));
      conditionCount += filter.views.length;
    }
    if (!conditionCount) return invalid('Minion filters need conditions.');
    return filter;
  };

  return parseNode(value, 0);
}

function parseQuery(value: unknown, viewExists: ViewChecker): MinionQuery {
  if (
    !isRecord(value) ||
    Object.keys(value).some(
      (key) =>
        ![
          'ids',
          'episodes',
          'seasons',
          'scenes',
          'cards',
          'rel',
          'filter',
          'random',
          'view',
        ].includes(key),
    )
  ) {
    return invalid('Invalid minion query.');
  }
  const query: MinionQuery = {};
  (['ids', 'episodes', 'seasons', 'scenes', 'cards'] as const).forEach(
    (key) => {
      if (value[key] !== undefined) query[key] = ids(value[key]);
    },
  );
  if (value.rel !== undefined) {
    if (
      typeof value.rel !== 'string' ||
      !/^[a-zA-Z0-9_-]{1,32}$/.test(value.rel) ||
      !query.cards
    ) {
      return invalid('Invalid card relation.');
    }
    query.rel = value.rel;
  }
  if (value.filter !== undefined) query.filter = parseFilter(value.filter);
  if (value.random !== undefined) {
    if (typeof value.random !== 'boolean') {
      return invalid('Invalid random query option.');
    }
    query.random = value.random;
  }
  if (value.view !== undefined) {
    if (
      typeof value.view !== 'string' ||
      !/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(value.view) ||
      Object.keys(query).some((key) => key !== 'view') ||
      !viewExists(value.view)
    ) {
      return invalid('Unknown or incompatible database view.');
    }
    query.view = value.view;
  }
  return query;
}

function rows<T>(value: unknown): T[] {
  if (!Array.isArray(value)) throw new Error('Unexpected database response.');
  return value as T[];
}

export default function createDbHandlers(
  run: Runner,
  trusted: Guard,
  viewExists: ViewChecker,
) {
  const execute = <T>(event: unknown, action: () => T): IpcResult<T> => {
    if (!trusted(event)) {
      return {
        ok: false,
        error: { code: 'UNAVAILABLE', message: 'Request unavailable.' },
      };
    }
    try {
      return { ok: true, data: action() };
    } catch (error) {
      const code: IpcErrorCode =
        error instanceof RequestError ? 'INVALID_REQUEST' : 'DATABASE_ERROR';
      return {
        ok: false,
        error: {
          code,
          message:
            code === 'INVALID_REQUEST' && error instanceof Error
              ? error.message
              : 'Could not load data.',
        },
      };
    }
  };

  return {
    labels: (event: unknown): IpcResult<LabelRow[]> =>
      execute(event, () =>
        rows<LabelRow>(run({ operation: DB_OPERATIONS.INITIALIZE_LABELS })),
      ),
    categories: (event: unknown, kind: unknown): IpcResult<CategoryRow[]> =>
      execute(event, () => {
        const operations: Record<
          CategoryKind,
          | DB_OPERATIONS.GET_TAG_CATEGORIES
          | DB_OPERATIONS.GET_IMPLEMENTATION_CATEGORIES
          | DB_OPERATIONS.GET_SCENES
          | DB_OPERATIONS.GET_EPISODES
        > = {
          tags: DB_OPERATIONS.GET_TAG_CATEGORIES,
          implementations: DB_OPERATIONS.GET_IMPLEMENTATION_CATEGORIES,
          scenes: DB_OPERATIONS.GET_SCENES,
          episodes: DB_OPERATIONS.GET_EPISODES,
        };
        if (typeof kind !== 'string' || !Object.hasOwn(operations, kind)) {
          return invalid('Unknown category type.');
        }
        return rows<CategoryRow>(
          run({ operation: operations[kind as CategoryKind] }),
        );
      }),
    cards: (event: unknown, value: unknown): IpcResult<CardRow[]> =>
      execute(event, () =>
        rows<CardRow>(
          run({
            operation: DB_OPERATIONS.GET_CARDS,
            query: { ids: ids(value) },
          }),
        ),
      ),
    minions: (
      event: unknown,
      value: unknown,
      page: unknown,
    ): IpcResult<MinionRow[]> =>
      execute(event, () => {
        if (
          !Number.isSafeInteger(page) ||
          (page as number) < 0 ||
          (page as number) > 1000000
        ) {
          return invalid('Page must be a nonnegative integer.');
        }
        return rows<MinionRow>(
          run({
            operation: DB_OPERATIONS.GET_MINIONS,
            query: parseQuery(value, viewExists),
            page: page as number,
          }),
        );
      }),
    minionCount: (event: unknown, value: unknown): IpcResult<number> =>
      execute(event, () => {
        const response = rows<{ total: number }>(
          run({
            operation: DB_OPERATIONS.GET_MINIONS_COUNT,
            query: parseQuery(value, viewExists),
          }),
        );
        if (
          !response.length ||
          !Number.isSafeInteger(response[0]?.total) ||
          response[0].total < 0
        ) {
          throw new Error('Invalid database count.');
        }
        return response[0].total;
      }),
    updateCardFilter: (
      event: unknown,
      cardId: unknown,
      filter: unknown,
    ): IpcResult<boolean> =>
      execute(event, () =>
        changed(
          run({
            operation: DB_OPERATIONS.UPDATE_CARD_FILTER,
            cardId: identifier(cardId, 'Card ID'),
            filter: parseFilter(filter),
          }),
        ),
      ),
    minionCards: (
      event: unknown,
      minionId: unknown,
    ): IpcResult<MinionCardRow[]> =>
      execute(event, () =>
        rows<MinionCardRow>(
          run({
            operation: DB_OPERATIONS.GET_MINION_CARDS,
            minionId: identifier(minionId, 'Minion ID'),
          }),
        ),
      ),
    cardSubs: (event: unknown, cardId: unknown): IpcResult<CardSubRow[]> =>
      execute(event, () =>
        rows<CardSubRow>(
          run({
            operation: DB_OPERATIONS.GET_CARD_SUBS,
            cardId: identifier(cardId, 'Card ID'),
          }),
        ),
      ),
    createCard: (
      event: unknown,
      parentId: unknown,
      name: unknown,
    ): IpcResult<boolean> =>
      execute(event, () =>
        changed(
          run({
            operation: DB_OPERATIONS.CREATE_CARD,
            parentId: identifier(parentId, 'Parent card ID'),
            name: cardName(name),
          }),
        ),
      ),
    renameCard: (
      event: unknown,
      cardId: unknown,
      name: unknown,
    ): IpcResult<boolean> =>
      execute(event, () =>
        changed(
          run({
            operation: DB_OPERATIONS.RENAME_CARD,
            cardId: identifier(cardId, 'Card ID'),
            name: cardName(name),
          }),
        ),
      ),
    deleteCard: (event: unknown, cardId: unknown): IpcResult<boolean> =>
      execute(event, () =>
        changed(
          run({
            operation: DB_OPERATIONS.DELETE_CARD,
            cardId: identifier(cardId, 'Card ID'),
          }),
        ),
      ),
  };
}
