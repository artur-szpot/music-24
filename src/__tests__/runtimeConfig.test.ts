import fs from 'fs';
import os from 'os';
import path from 'path';
import {
  loadRuntimeConfig,
  resolveAssetPath,
  RuntimeConfig,
  saveRuntimeConfig,
  validateRuntimeConfig,
} from '../main/runtimeConfig';

describe('runtime configuration', () => {
  let tempRoot: string;
  let config: RuntimeConfig;

  beforeEach(() => {
    tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'minion-decider-'));
    const databasePath = path.join(tempRoot, 'collection.db');
    const minionRoot = path.join(tempRoot, 'minions');
    const cardRoot = path.join(tempRoot, 'cards');
    const fileSystemRoot = path.join(tempRoot, 'files');
    fs.writeFileSync(databasePath, 'fixture');
    [minionRoot, cardRoot, fileSystemRoot].forEach((directory) =>
      fs.mkdirSync(directory),
    );
    config = { databasePath, minionRoot, cardRoot, fileSystemRoot };
  });

  afterEach(() => {
    fs.rmSync(tempRoot, { recursive: true, force: true });
  });

  it('validates accessible files and directories', () => {
    expect(validateRuntimeConfig(config)).toEqual({ config, errors: [] });
  });

  it('rejects missing and incorrectly typed paths', () => {
    const result = validateRuntimeConfig({
      ...config,
      databasePath: config.minionRoot,
      cardRoot: path.join(tempRoot, 'missing'),
    });

    expect(result.config).toBeUndefined();
    expect(result.errors).toEqual([
      'Database must point to a file.',
      'Card image root does not exist or cannot be accessed.',
    ]);
  });

  it('persists and reloads a valid configuration', () => {
    const configPath = path.join(tempRoot, 'settings', 'runtime-config.json');
    saveRuntimeConfig(configPath, config);

    expect(loadRuntimeConfig(configPath)).toEqual({ config, errors: [] });
  });

  it('resolves asset paths within their configured root', () => {
    expect(resolveAssetPath(config.minionRoot, 'minion:///1/image.png')).toBe(
      path.join(config.minionRoot, '1', 'image.png'),
    );
  });

  it('rejects asset paths that escape their configured root', () => {
    expect(() =>
      resolveAssetPath(config.minionRoot, 'minion:///..%2Fsecret.png'),
    ).toThrow('Asset request is outside the configured root.');
  });
});
