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

  it('keeps the previous configuration when a replacement is invalid', () => {
    const configPath = path.join(tempRoot, 'runtime-config.json');
    saveRuntimeConfig(configPath, config);
    const original = fs.readFileSync(configPath, 'utf8');

    expect(() =>
      saveRuntimeConfig(configPath, {
        ...config,
        cardRoot: path.join(tempRoot, 'missing'),
      }),
    ).toThrow();
    expect(fs.readFileSync(configPath, 'utf8')).toBe(original);
  });

  it('keeps the previous configuration if the atomic replacement fails', () => {
    const configPath = path.join(tempRoot, 'runtime-config.json');
    saveRuntimeConfig(configPath, config);
    const original = fs.readFileSync(configPath, 'utf8');
    const otherRoot = path.join(tempRoot, 'other');
    fs.mkdirSync(otherRoot);
    const rename = jest.spyOn(fs, 'renameSync').mockImplementationOnce(() => {
      throw new Error('rename failed');
    });
    try {
      expect(() =>
        saveRuntimeConfig(configPath, { ...config, cardRoot: otherRoot }),
      ).toThrow('rename failed');
      expect(fs.readFileSync(configPath, 'utf8')).toBe(original);
      expect(
        fs.readdirSync(tempRoot).filter((name) => name.endsWith('.tmp')),
      ).toEqual([]);
    } finally {
      rename.mockRestore();
    }
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
