import {
  CardRow,
  CategoryKind,
  CategoryRow,
  IpcErrorCode,
  IpcResult,
  LabelRow,
  MinionQuery,
  MinionRow,
} from '../constants/dbIpc';
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
    value.length > 500 ||
    !value.every((id) => Number.isSafeInteger(id) && id >= 0)
  ) {
    return invalid(
      'IDs must be a nonempty list of at most 500 nonnegative integers.',
    );
  }
  return value;
}

function parseQuery(value: unknown, viewExists: ViewChecker): MinionQuery {
  if (
    !isRecord(value) ||
    Object.keys(value).some(
      (key) =>
        !['ids', 'episodes', 'scenes', 'cards', 'rel', 'view'].includes(key),
    )
  ) {
    return invalid('Invalid minion query.');
  }
  const query: MinionQuery = {};
  (['ids', 'episodes', 'scenes', 'cards'] as const).forEach((key) => {
    if (value[key] !== undefined) query[key] = ids(value[key]);
  });
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
  if (value.view !== undefined) {
    if (
      typeof value.view !== 'string' ||
      !/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(value.view) ||
      Object.keys(query).length ||
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
  };
}
