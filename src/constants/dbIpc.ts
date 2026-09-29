export const DB_CHANNELS = {
  LABELS: 'db:labels',
  CATEGORIES: 'db:categories',
  CARDS: 'db:cards',
  MINIONS: 'db:minions',
  MINION_COUNT: 'db:minion-count',
} as const;

export type CategoryKind = 'tags' | 'implementations' | 'scenes' | 'episodes';

export interface MinionQuery {
  episodes?: number[];
  ids?: number[];
  scenes?: number[];
  cards?: number[];
  rel?: string;
  view?: string;
}

export interface MinionRow {
  id: number;
  url: string;
  episode: number;
  scene: number;
}

export interface CardRow {
  id: number;
  name: string;
  parent: number | null;
  category: string | null;
  cardType: string;
  view: string | null;
}

export interface CategoryRow {
  id: number;
  name: string;
  parent: number | null;
  category: string;
  total: number;
  episode?: number | null;
}

export interface LabelRow {
  id: number;
  name: string;
  category: 'card' | 'scene' | 'episode';
}

export type IpcErrorCode = 'INVALID_REQUEST' | 'UNAVAILABLE' | 'DATABASE_ERROR';

export type IpcResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: { code: IpcErrorCode; message: string } };
