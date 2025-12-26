/* eslint global-require: off, no-console: off, promise/always-return: off */

/**
 * This module executes inside of electron's main process. You can start
 * electron renderer process from here and communicate with the other processes
 * through IPC.
 *
 * When running `npm run build` or `npm run build:main`, this file is compiled to
 * `./src/main.js` using webpack. This gives us some performance wins.
 */
import { app, BrowserWindow, ipcMain, net, protocol, shell } from 'electron';
import path from 'path';
import url from 'url';
import { dbOperation } from './db';
import MenuBuilder from './menu';
import { resolveHtmlPath } from './util';

export const QUERY_CHANNEL = 'query-channel';
export const COUNT_CHANNEL = 'count-channel';

let mainWindow: BrowserWindow | null = null;

// Forward a DB operation to its handler
ipcMain.on(QUERY_CHANNEL, async (event, arg) => {
  event.reply(QUERY_CHANNEL, dbOperation(arg));
});
ipcMain.on(COUNT_CHANNEL, async (event, arg) => {
  event.reply(COUNT_CHANNEL, dbOperation(arg));
});

if (process.env.NODE_ENV === 'production') {
  const sourceMapSupport = require('source-map-support');
  sourceMapSupport.install();
}

const isDebug =
  process.env.NODE_ENV === 'development' || process.env.DEBUG_PROD === 'true';

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
  .then(() => {
    protocol.handle('minion', (request) => {
      const srcPath = 'E:\\programming\\ponypics\\s\\';
      const reqURL = new URL(request.url);
      return net.fetch(
        url.pathToFileURL(path.join(srcPath, reqURL.pathname)).toString(),
      );
    });
    protocol.handle('card', (request) => {
      const srcPath = 'E:\\programming\\ponypics\\cards\\';
      const reqURL = new URL(request.url);
      return net.fetch(
        url.pathToFileURL(path.join(srcPath, reqURL.pathname)).toString(),
      );
    });
    protocol.handle('file-system', (request) => {
      const srcPath = 'C:\\Users\\szpot\\Downloads\\';
      const reqURL = new URL(request.url);
      return net.fetch(
        url.pathToFileURL(path.join(srcPath, reqURL.pathname)).toString(),
      );
    });

    createWindow();
    app.on('activate', () => {
      // On macOS it's common to re-create a window in the app when the
      // dock icon is clicked and there are no other windows open.
      if (mainWindow === null) createWindow();
    });
  })
  .catch(console.log);
