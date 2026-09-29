import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { RuntimeConfig } from '../constants/runtimeConfig';
import createMinionFileHandlers from '../main/minionFileHandlers';

describe('minion file handlers', () => {
  let root: string;
  let config: RuntimeConfig;
  const sender = {};
  const trusted = (event: unknown) => event === sender;

  beforeEach(() => {
    root = fs.mkdtempSync(path.join(os.tmpdir(), 'minion-files-'));
    const minionRoot = path.join(root, 'minions');
    const outputDirectory = path.join(root, 'output');
    fs.mkdirSync(path.join(minionRoot, '2'), { recursive: true });
    fs.mkdirSync(outputDirectory);
    fs.writeFileSync(path.join(minionRoot, '2', 'sample image.png'), 'image');
    config = {
      databasePath: path.join(root, 'collection.db'),
      minionRoot,
      cardRoot: root,
      fileSystemRoot: root,
      outputDirectory,
    };
  });

  afterEach(() => {
    fs.rmSync(root, { recursive: true, force: true });
  });

  it('returns and reveals only a source resolved from the minion ID', async () => {
    const reveal = jest.fn();
    const handlers = createMinionFileHandlers(
      () => ({
        id: 3,
        url: 'sample image.png',
        episode: 2,
        scene: 1,
        season: 1,
      }),
      trusted,
      () => config,
      reveal,
    );

    const source = await handlers.source(sender, 3);
    expect(source).toEqual({
      ok: true,
      data: {
        fileName: 'sample image.png',
        fullPath: path.join(config.minionRoot, '2', 'sample image.png'),
      },
    });
    expect(await handlers.reveal(sender, 3)).toEqual({ ok: true, data: true });
    expect(reveal).toHaveBeenCalledWith(source.ok ? source.data.fullPath : '');
  });

  it('copies without overwriting and reports a destination conflict', async () => {
    const handlers = createMinionFileHandlers(
      () => ({
        id: 3,
        url: 'sample image.png',
        episode: 2,
        scene: 1,
        season: 1,
      }),
      trusted,
      () => config,
      jest.fn(),
    );

    expect(await handlers.copy(sender, 3)).toEqual({ ok: true, data: true });
    const destination = path.join(config.outputDirectory!, 'sample image.png');
    expect(fs.readFileSync(destination, 'utf8')).toBe('image');
    fs.writeFileSync(destination, 'existing');
    expect(await handlers.copy(sender, 3)).toEqual({
      ok: false,
      error: {
        code: 'CONFLICT',
        message:
          'A file with that name already exists in the output directory.',
      },
    });
    expect(fs.readFileSync(destination, 'utf8')).toBe('existing');
  });

  it('rejects untrusted, missing, and traversal source requests', async () => {
    const handlers = createMinionFileHandlers(
      (id) =>
        id === 4
          ? { id, url: '../outside.png', episode: 2, scene: 1, season: 1 }
          : undefined,
      trusted,
      () => config,
      jest.fn(),
    );

    expect(await handlers.source({}, 3)).toMatchObject({
      ok: false,
      error: { code: 'UNAVAILABLE' },
    });
    expect(await handlers.source(sender, 3)).toMatchObject({
      ok: false,
      error: { code: 'NOT_FOUND' },
    });
    expect(await handlers.source(sender, 4)).toMatchObject({
      ok: false,
      error: { code: 'NOT_FOUND' },
    });
  });

  it('requires an output directory before copying', async () => {
    const handlers = createMinionFileHandlers(
      () => ({
        id: 3,
        url: 'sample image.png',
        episode: 2,
        scene: 1,
        season: 1,
      }),
      trusted,
      () => ({ ...config, outputDirectory: undefined }),
      jest.fn(),
    );

    expect(await handlers.copy(sender, 3)).toMatchObject({
      ok: false,
      error: { code: 'NOT_CONFIGURED' },
    });
  });
});
