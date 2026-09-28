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
  net,
  protocol,
  shell,
} from 'electron';
import path from 'path';
import url from 'url';
import { dbOperation, initializeDatabase } from './db';
import MenuBuilder from './menu';
import {
  loadRuntimeConfig,
  resolveAssetPath,
  RUNTIME_CONFIG_FILENAME,
  RuntimeConfig,
  saveRuntimeConfig,
  validateRuntimeConfig,
} from './runtimeConfig';
import { resolveHtmlPath } from './util';

export const DEFAULT_CHANNEL = 'default-channel';

let mainWindow: BrowserWindow | null = null;

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
  const configPath = path.join(
    app.getPath('userData'),
    RUNTIME_CONFIG_FILENAME,
  );
  const saved = loadRuntimeConfig(configPath);
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
    saveRuntimeConfig(configPath, validation.config);
    return validation.config;
  } catch (error) {
    dialog.showErrorBox(
      'Could not save Minion Decider configuration',
      error instanceof Error ? error.message : String(error),
    );
    return undefined;
  }
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
