import { constants } from 'node:fs';
import { copyFile, stat } from 'node:fs/promises';
import path from 'node:path';
import {
  IpcErrorCode,
  IpcResult,
  MinionRow,
  MinionSource,
} from '../constants/dbIpc';
import { RuntimeConfig } from '../constants/runtimeConfig';
import { resolveAssetPath } from './runtimeConfig';

type Guard = (event: unknown) => boolean;
type MinionLookup = (id: number) => MinionRow | undefined;
type ConfigLookup = () => RuntimeConfig | undefined;
type CopyOperation = (source: string, destination: string) => Promise<void>;
type RevealOperation = (source: string) => void;
type RequestValidation = { id: number } | { result: IpcResult<never> };

function failure<T>(code: IpcErrorCode, message: string): IpcResult<T> {
  return { ok: false, error: { code, message } };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

export default function createMinionFileHandlers(
  lookupMinion: MinionLookup,
  trusted: Guard,
  getConfig: ConfigLookup,
  reveal: RevealOperation,
  copy: CopyOperation = (source, destination) =>
    copyFile(source, destination, constants.COPYFILE_EXCL),
) {
  const resolveSource = async (
    id: number,
  ): Promise<MinionSource | undefined> => {
    const config = getConfig();
    if (!config) throw new Error('Configuration unavailable.');
    const minion = lookupMinion(id);
    if (
      !minion ||
      !Number.isSafeInteger(minion.episode) ||
      typeof minion.url !== 'string'
    ) {
      return undefined;
    }
    const sourcePath = resolveAssetPath(
      config.minionRoot,
      `minion:///${minion.episode}/${encodeURIComponent(minion.url)}`,
    );
    const file = await stat(sourcePath);
    if (!file.isFile()) return undefined;
    return { fileName: path.basename(sourcePath), fullPath: sourcePath };
  };

  const validateRequest = (event: unknown, id: unknown): RequestValidation => {
    if (!trusted(event)) {
      return { result: failure('UNAVAILABLE', 'Request unavailable.') };
    }
    if (!Number.isSafeInteger(id) || (id as number) < 0) {
      return {
        result: failure(
          'INVALID_REQUEST',
          'Minion ID must be a nonnegative integer.',
        ),
      };
    }
    return { id: id as number };
  };

  return {
    source: async (
      event: unknown,
      id: unknown,
    ): Promise<IpcResult<MinionSource>> => {
      const request = validateRequest(event, id);
      if ('result' in request) return request.result;
      try {
        const source = await resolveSource(request.id);
        return source
          ? { ok: true, data: source }
          : failure('NOT_FOUND', 'Minion source file was not found.');
      } catch {
        return failure('NOT_FOUND', 'Minion source file was not found.');
      }
    },
    reveal: async (
      event: unknown,
      id: unknown,
    ): Promise<IpcResult<boolean>> => {
      const request = validateRequest(event, id);
      if ('result' in request) return request.result;
      try {
        const source = await resolveSource(request.id);
        if (!source)
          return failure('NOT_FOUND', 'Minion source file was not found.');
        reveal(source.fullPath);
        return { ok: true, data: true };
      } catch {
        return failure('NOT_FOUND', 'Minion source file was not found.');
      }
    },
    copy: async (event: unknown, id: unknown): Promise<IpcResult<boolean>> => {
      const request = validateRequest(event, id);
      if ('result' in request) return request.result;
      const config = getConfig();
      if (!config) return failure('UNAVAILABLE', 'Configuration unavailable.');
      if (!config.outputDirectory) {
        return failure(
          'NOT_CONFIGURED',
          'Choose an output directory in Settings before copying minions.',
        );
      }
      try {
        const source = await resolveSource(request.id);
        if (!source)
          return failure('NOT_FOUND', 'Minion source file was not found.');
        const outputStats = await stat(config.outputDirectory);
        if (!outputStats.isDirectory()) {
          return failure(
            'NOT_CONFIGURED',
            'The output directory is unavailable.',
          );
        }
        await copy(
          source.fullPath,
          path.join(config.outputDirectory, source.fileName),
        );
        return { ok: true, data: true };
      } catch (error) {
        if (isRecord(error) && error.code === 'EEXIST') {
          return failure(
            'CONFLICT',
            'A file with that name already exists in the output directory.',
          );
        }
        return failure('UNAVAILABLE', 'Could not copy the minion file.');
      }
    },
  };
}
