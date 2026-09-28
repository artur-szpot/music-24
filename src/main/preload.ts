// Disable no-unused-vars, broken for spread args
/* eslint no-unused-vars: off */
import { contextBridge, ipcRenderer, IpcRendererEvent } from 'electron';
import {
  CONFIG_CHANNELS,
  ConfigUpdateResult,
  RuntimeConfig,
  RuntimeConfigKey,
} from '../constants/runtimeConfig';

// export type Channels = 'default-channel' | 'count-channel';

const electronHandler = {
  config: {
    get(): Promise<RuntimeConfig> {
      return ipcRenderer.invoke(CONFIG_CHANNELS.GET);
    },
    choose(key: RuntimeConfigKey): Promise<string | null> {
      return ipcRenderer.invoke(CONFIG_CHANNELS.CHOOSE, key);
    },
    apply(config: RuntimeConfig): Promise<ConfigUpdateResult> {
      return ipcRenderer.invoke(CONFIG_CHANNELS.APPLY, config);
    },
  },
  ipcRenderer: {
    sendMessage(channel: string, ...args: unknown[]) {
      ipcRenderer.send(channel, ...args);
    },
    on(channel: string, func: (...args: unknown[]) => void) {
      const subscription = (_event: IpcRendererEvent, ...args: unknown[]) =>
        func(...args);
      ipcRenderer.on(channel, subscription);

      return () => {
        ipcRenderer.removeListener(channel, subscription);
      };
    },
    once(channel: string, func: (...args: unknown[]) => void) {
      ipcRenderer.once(channel, (_event, ...args) => func(...args));
    },
  },
};

contextBridge.exposeInMainWorld('electron', electronHandler);

export type ElectronHandler = typeof electronHandler;
