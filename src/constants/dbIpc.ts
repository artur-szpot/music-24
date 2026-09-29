export const DB_CHANNELS = {
  LABELS: 'db:labels',
  CATEGORIES: 'db:categories',
  CARDS: 'db:cards',
  MINIONS: 'db:minions',
  MINION_COUNT: 'db:minion-count',
  UPDATE_CARD_FILTER: 'db:update-card-filter',
  MINION_CARDS: 'db:minion-cards',
  MINION_SOURCE: 'db:minion-source',
  REVEAL_MINION: 'db:reveal-minion',
  COPY_MINION: 'db:copy-minion',
} as const;

export type CategoryKind = 'tags' | 'implementations' | 'scenes' | 'episodes';

export interface FilterCategory {
  oneOf?: number[];
  allOf?: number[];
  noneOf?: number[];
}

export interface MinionFilter {
  logic: 'any' | 'all';
  cards?: FilterCategory;
  seasons?: FilterCategory;
  episodes?: FilterCategory;
  scenes?: FilterCategory;
  views?: MinionFilter[];
}

export interface MinionQuery {
  episodes?: number[];
  ids?: number[];
  seasons?: number[];
  scenes?: number[];
  cards?: number[];
  rel?: string;
  filter?: MinionFilter;
  random?: boolean;
  view?: string;
}

export interface MinionRow {
  id: number;
  url: string;
  episode: number;
  scene: number;
  season: number | null;
}

export interface MinionCardRow {
  id: number;
  name: string;
  parent: number | null;
  category: string | null;
  cardType: string;
  isSelected: number;
}

export interface MinionSource {
  fileName: string;
  fullPath: string;
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

export type IpcErrorCode =
  | 'INVALID_REQUEST'
  | 'UNAVAILABLE'
  | 'DATABASE_ERROR'
  | 'NOT_FOUND'
  | 'NOT_CONFIGURED'
  | 'CONFLICT';

export type IpcResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: { code: IpcErrorCode; message: string } };
