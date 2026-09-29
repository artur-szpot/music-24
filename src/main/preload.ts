import { contextBridge, ipcRenderer } from 'electron';
import {
  CardRow,
  CategoryKind,
  CategoryRow,
  DB_CHANNELS,
  IpcResult,
  LabelRow,
  MinionQuery,
  MinionRow,
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
  },
};

contextBridge.exposeInMainWorld('electron', electronHandler);

export type ElectronHandler = typeof electronHandler;
