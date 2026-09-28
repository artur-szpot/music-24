/* eslint global-require: off, no-console: off, promise/always-return: off */

/**
 * This module executes inside of electron's main process. You can start
 * electron renderer process from here and communicate with the other processes
 * through IPC.
 *
 * When running `npm run build` or `npm run build:main`, this file is compiled to
 * `./src/main.js` using webpack. This gives us some performance wins.
 */
import {
  app,
  BrowserWindow,
  dialog,
  ipcMain,
  IpcMainInvokeEvent,
  net,
  protocol,
  shell,
} from 'electron';
import path from 'path';
import url from 'url';
import Database from 'better-sqlite3';
import {
  CONFIG_CHANNELS,
  ConfigUpdateResult,
  RuntimeConfig,
} from '../constants/runtimeConfig';
import { dbOperation, initializeDatabase } from './db';
import MenuBuilder from './menu';
import {
  loadRuntimeConfig,
  resolveAssetPath,
  RUNTIME_CONFIG_FILENAME,
  saveRuntimeConfig,
  validateRuntimeConfig,
} from './runtimeConfig';
import { resolveHtmlPath } from './util';

export const DEFAULT_CHANNEL = 'default-channel';

let mainWindow: BrowserWindow | null = null;
let activeConfig: RuntimeConfig | undefined;
let restartPending = false;

const configPath = () =>
  path.join(app.getPath('userData'), RUNTIME_CONFIG_FILENAME);

// Forward a DB operation to its handler
ipcMain.on(DEFAULT_CHANNEL, async (event, arg) => {
  if (arg.privateChannel) {
    event.reply(arg.privateChannel, dbOperation(arg));
  } else if (arg.log) {
    console.log(arg.log);
  }
});

if (process.env.NODE_ENV === 'production') {
  const sourceMapSupport = require('source-map-support');
  sourceMapSupport.install();
}

const isDebug =
  process.env.NODE_ENV === 'development' || process.env.DEBUG_PROD === 'true';

const selectFile = async (
  title: string,
  defaultPath?: string,
): Promise<string | undefined> => {
  const result = await dialog.showOpenDialog({
    title,
    defaultPath,
    properties: ['openFile'],
    filters: [
      { name: 'SQLite databases', extensions: ['db', 'sqlite', 'sqlite3'] },
      { name: 'All files', extensions: ['*'] },
    ],
  });
  return result.canceled ? undefined : result.filePaths[0];
};

const selectDirectory = async (
  title: string,
  defaultPath?: string,
): Promise<string | undefined> => {
  const result = await dialog.showOpenDialog({
    title,
    defaultPath,
    properties: ['openDirectory'],
  });
  return result.canceled ? undefined : result.filePaths[0];
};

const promptForRuntimeConfig = async (
  previous?: RuntimeConfig,
): Promise<RuntimeConfig | undefined> => {
  const databasePath = await selectFile(
    'Select the Minion Decider SQLite database',
    previous?.databasePath,
  );
  if (!databasePath) return undefined;

  const minionRoot = await selectDirectory(
    'Select the minion image root directory',
    previous?.minionRoot,
  );
  if (!minionRoot) return undefined;

  const cardRoot = await selectDirectory(
    'Select the card image root directory',
    previous?.cardRoot,
  );
  if (!cardRoot) return undefined;

  const fileSystemRoot = await selectDirectory(
    'Select the general file-system image root directory',
    previous?.fileSystemRoot,
  );
  if (!fileSystemRoot) return undefined;

  return { databasePath, minionRoot, cardRoot, fileSystemRoot };
};

const ensureRuntimeConfig = async (): Promise<RuntimeConfig | undefined> => {
  const saved = loadRuntimeConfig(configPath());
  const forceConfiguration = process.argv.includes('--configure');

  if (saved.config && !forceConfiguration) {
    return saved.config;
  }

  const response = await dialog.showMessageBox({
    type: saved.config ? 'info' : 'warning',
    title: 'Configure Minion Decider',
    message: saved.config
      ? 'Choose the database and image directories to use.'
      : 'Minion Decider needs a valid database and image directories before it can start.',
    detail: saved.config ? undefined : saved.errors.join('\n'),
    buttons: ['Configure', 'Quit'],
    defaultId: 0,
    cancelId: 1,
    noLink: true,
  });
  if (response.response !== 0) return undefined;

  const selected = await promptForRuntimeConfig(saved.config);
  if (!selected) return undefined;

  const validation = validateRuntimeConfig(selected);
  if (!validation.config) {
    dialog.showErrorBox(
      'Invalid Minion Decider configuration',
      validation.errors.join('\n'),
    );
    return undefined;
  }

  try {
    saveRuntimeConfig(configPath(), validation.config);
    return validation.config;
  } catch (error) {
    dialog.showErrorBox(
      'Could not save Minion Decider configuration',
      error instanceof Error ? error.message : String(error),
    );
    return undefined;
  }
};

const validateDatabaseForSwitch = (
  databasePath: string,
): string | undefined => {
  let probe: Database.Database | undefined;
  try {
    probe = new Database(databasePath, { readonly: true, fileMustExist: true });
    probe.prepare('select id, url, episode, scene from minions limit 0');
    probe.prepare('select id, name from cards limit 0');
    probe.prepare('select id, name from episodes limit 0');
    probe.prepare('select id, name from scenes limit 0');
    probe.prepare(
      'select card_id, rel, total from minion_card_relations_counts limit 0',
    );
    probe.prepare('select episode, total from minion_episodes_counts limit 0');
    probe.prepare('select scene, total from minion_scenes_counts limit 0');
    return undefined;
  } catch {
    return 'The selected database could not be opened read-only or is missing required columns.';
  } finally {
    probe?.close();
  }
};

const registerConfigurationHandlers = (): void => {
  const fromWindow = (event: IpcMainInvokeEvent) =>
    event.sender === mainWindow?.webContents &&
    event.senderFrame === mainWindow.webContents.mainFrame;

  ipcMain.handle(CONFIG_CHANNELS.GET, (event) => {
    if (!fromWindow(event) || !activeConfig) throw new Error('Unavailable.');
    return activeConfig;
  });

  ipcMain.handle(CONFIG_CHANNELS.CHOOSE, async (event, key: unknown) => {
    if (!fromWindow(event) || !activeConfig || restartPending) {
      throw new Error('Unavailable.');
    }
    switch (key) {
      case 'databasePath':
        return (
          (await selectFile(
            'Select the Minion Decider SQLite database',
            activeConfig.databasePath,
          )) ?? null
        );
      case 'minionRoot':
      case 'cardRoot':
      case 'fileSystemRoot':
        return (
          (await selectDirectory(
            'Select image root directory',
            activeConfig[key],
          )) ?? null
        );
      default:
        throw new Error('Invalid configuration path type.');
    }
  });

  ipcMain.handle(
    CONFIG_CHANNELS.APPLY,
    (event, candidate: unknown): ConfigUpdateResult => {
      if (!fromWindow(event) || !activeConfig || restartPending) {
        return { restarting: false, errors: ['Configuration is unavailable.'] };
      }
      const validated = validateRuntimeConfig(candidate);
      if (!validated.config) {
        return { restarting: false, errors: validated.errors };
      }
      const next = validated.config;
      const previous = activeConfig;
      if (
        Object.keys(previous).every(
          (key) =>
            previous[key as keyof RuntimeConfig] ===
            next[key as keyof RuntimeConfig],
        )
      ) {
        return { restarting: false, errors: [] };
      }
      if (next.databasePath !== previous.databasePath) {
        const error = validateDatabaseForSwitch(next.databasePath);
        if (error) return { restarting: false, errors: [error] };
      }
      try {
        saveRuntimeConfig(configPath(), next);
      } catch (error) {
        return {
          restarting: false,
          errors: [
            error instanceof Error
              ? error.message
              : 'Could not save configuration.',
          ],
        };
      }

      restartPending = true;
      // Restart, rather than hot-swapping SQLite and protocol handlers while
      // renderer requests may still be in flight. Return the IPC result first.
      setTimeout(() => {
        try {
          app.relaunch({
            args: process.argv.slice(1).filter((arg) => arg !== '--configure'),
          });
          app.quit();
        } catch {
          restartPending = false;
          try {
            saveRuntimeConfig(configPath(), previous);
            dialog.showErrorBox(
              'Restart failed',
              'Previous configuration restored.',
            );
          } catch {
            dialog.showErrorBox(
              'Restart failed',
              'Could not restore the previous configuration. Reconfigure on next launch.',
            );
          }
        }
      }, 100);
      return { restarting: true, errors: [] };
    },
  );
};

const registerAssetProtocol = (scheme: string, root: string): void => {
  protocol.handle(scheme, (request) => {
    try {
      const assetPath = resolveAssetPath(root, request.url);
      return net.fetch(url.pathToFileURL(assetPath).toString());
    } catch {
      return new Response('Invalid asset path.', { status: 400 });
    }
  });
};

// if (isDebug) {
//   require('electron-debug').default();
// }

const installExtensions = async () => {
  const installer = require('electron-devtools-installer');
  const forceDownload = !!process.env.UPGRADE_EXTENSIONS;
  const extensions = ['REACT_DEVELOPER_TOOLS'];

  return installer
    .default(
      extensions.map((name) => installer[name]),
      forceDownload,
    )
    .catch(console.log);
};

const createWindow = async () => {
  if (isDebug) {
    await installExtensions();
  }

  const RESOURCES_PATH = app.isPackaged
    ? path.join(process.resourcesPath, 'assets')
    : path.join(__dirname, '../../assets');

  const getAssetPath = (...paths: string[]): string => {
    return path.join(RESOURCES_PATH, ...paths);
  };

  mainWindow = new BrowserWindow({
    show: false,
    //  width: 1024,
    //  height: 728,
    icon: getAssetPath('icon.png'),
    webPreferences: {
      preload: app.isPackaged
        ? path.join(__dirname, 'preload.js')
        : path.join(__dirname, '../../.erb/dll/preload.js'),
    },
  });

  mainWindow.loadURL(resolveHtmlPath('index.html'));
  mainWindow.maximize();

  mainWindow.on('ready-to-show', () => {
    if (!mainWindow) {
      throw new Error('"mainWindow" is not defined');
    }
    if (process.env.START_MINIMIZED) {
      mainWindow.minimize();
    } else {
      mainWindow.show();
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  const menuBuilder = new MenuBuilder(mainWindow);
  menuBuilder.buildMenu();

  // Open urls in the user's browser
  mainWindow.webContents.setWindowOpenHandler((edata) => {
    shell.openExternal(edata.url);
    return { action: 'deny' };
  });
};

app.on('window-all-closed', () => {
  // Respect the OSX convention of having the application in memory even
  // after all windows have been closed
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app
  .whenReady()
  .then(async () => {
    const runtimeConfig = await ensureRuntimeConfig();
    if (!runtimeConfig) {
      app.quit();
      return;
    }

    try {
      initializeDatabase(runtimeConfig.databasePath);
    } catch (error) {
      dialog.showErrorBox(
        'Could not open the Minion Decider database',
        error instanceof Error ? error.message : String(error),
      );
      app.quit();
      return;
    }

    activeConfig = runtimeConfig;
    registerConfigurationHandlers();

    registerAssetProtocol('minion', runtimeConfig.minionRoot);
    registerAssetProtocol('card', runtimeConfig.cardRoot);
    registerAssetProtocol('file-system', runtimeConfig.fileSystemRoot);

    await createWindow();
    app.on('activate', () => {
      // On macOS it's common to re-create a window in the app when the
      // dock icon is clicked and there are no other windows open.
      if (mainWindow === null) createWindow();
    });
  })
  .catch((error) => {
    console.error(error);
    app.quit();
  });
