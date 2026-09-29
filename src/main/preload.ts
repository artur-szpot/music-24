import { contextBridge, ipcRenderer } from 'electron';
import {
  CardRow,
  CategoryKind,
  CategoryRow,
  DB_CHANNELS,
  IpcResult,
  LabelRow,
  MinionCardRow,
  MinionFilter,
  MinionQuery,
  MinionRow,
  MinionSource,
} from '../constants/dbIpc';
import {
  CONFIG_CHANNELS,
  ConfigUpdateResult,
  RuntimeConfig,
  RuntimeConfigKey,
} from '../constants/runtimeConfig';

const electronHandler = {
  config: {
    get(): Promise<IpcResult<RuntimeConfig>> {
      return ipcRenderer.invoke(CONFIG_CHANNELS.GET);
    },
    choose(key: RuntimeConfigKey): Promise<IpcResult<string | null>> {
      return ipcRenderer.invoke(CONFIG_CHANNELS.CHOOSE, key);
    },
    apply(config: RuntimeConfig): Promise<ConfigUpdateResult> {
      return ipcRenderer.invoke(CONFIG_CHANNELS.APPLY, config);
    },
  },
  database: {
    labels(): Promise<IpcResult<LabelRow[]>> {
      return ipcRenderer.invoke(DB_CHANNELS.LABELS);
    },
    categories(kind: CategoryKind): Promise<IpcResult<CategoryRow[]>> {
      return ipcRenderer.invoke(DB_CHANNELS.CATEGORIES, kind);
    },
    cards(ids: number[]): Promise<IpcResult<CardRow[]>> {
      return ipcRenderer.invoke(DB_CHANNELS.CARDS, ids);
    },
    minions(query: MinionQuery, page: number): Promise<IpcResult<MinionRow[]>> {
      return ipcRenderer.invoke(DB_CHANNELS.MINIONS, query, page);
    },
    minionCount(query: MinionQuery): Promise<IpcResult<number>> {
      return ipcRenderer.invoke(DB_CHANNELS.MINION_COUNT, query);
    },
    updateCardFilter(
      cardId: number,
      filter: MinionFilter,
    ): Promise<IpcResult<boolean>> {
      return ipcRenderer.invoke(DB_CHANNELS.UPDATE_CARD_FILTER, cardId, filter);
    },
    minionCards(minionId: number): Promise<IpcResult<MinionCardRow[]>> {
      return ipcRenderer.invoke(DB_CHANNELS.MINION_CARDS, minionId);
    },
    minionSource(minionId: number): Promise<IpcResult<MinionSource>> {
      return ipcRenderer.invoke(DB_CHANNELS.MINION_SOURCE, minionId);
    },
    revealMinion(minionId: number): Promise<IpcResult<boolean>> {
      return ipcRenderer.invoke(DB_CHANNELS.REVEAL_MINION, minionId);
    },
    copyMinion(minionId: number): Promise<IpcResult<boolean>> {
      return ipcRenderer.invoke(DB_CHANNELS.COPY_MINION, minionId);
    },
  },
};

contextBridge.exposeInMainWorld('electron', electronHandler);

export type ElectronHandler = typeof electronHandler;
