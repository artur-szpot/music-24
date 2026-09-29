import fs from 'fs';
import path from 'path';
import { RuntimeConfig } from '../constants/runtimeConfig';

export type { RuntimeConfig } from '../constants/runtimeConfig';

export const RUNTIME_CONFIG_FILENAME = 'runtime-config.json';

export interface RuntimeConfigResult {
  config?: RuntimeConfig;
  errors: string[];
}

const CONFIG_KEYS: (keyof RuntimeConfig)[] = [
  'databasePath',
  'minionRoot',
  'cardRoot',
  'fileSystemRoot',
];

const CONFIG_LABELS: Partial<Record<keyof RuntimeConfig, string>> = {
  databasePath: 'Database',
  minionRoot: 'Minion image root',
  cardRoot: 'Card image root',
  fileSystemRoot: 'File-system image root',
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

export function validateRuntimeConfig(value: unknown): RuntimeConfigResult {
  if (!isRecord(value)) {
    return { errors: ['Configuration must be a JSON object.'] };
  }

  const errors: string[] = [];
  const candidate = {} as RuntimeConfig;

  CONFIG_KEYS.forEach((key) => {
    const configuredPath = value[key];
    const label = CONFIG_LABELS[key] ?? 'Output directory';

    if (typeof configuredPath !== 'string' || !configuredPath.trim()) {
      errors.push(`${label} must be configured.`);
      return;
    }
    if (!path.isAbsolute(configuredPath)) {
      errors.push(`${label} must be an absolute path.`);
      return;
    }

    const normalizedPath = path.normalize(configuredPath);
    candidate[key] = normalizedPath;

    try {
      const stats = fs.statSync(normalizedPath);
      const validType =
        key === 'databasePath' ? stats.isFile() : stats.isDirectory();
      if (!validType) {
        errors.push(
          `${label} must point to ${
            key === 'databasePath' ? 'a file' : 'a directory'
          }.`,
        );
      }
    } catch {
      errors.push(`${label} does not exist or cannot be accessed.`);
    }
  });

  if (value.outputDirectory !== undefined) {
    const outputDirectory = value.outputDirectory;
    if (typeof outputDirectory !== 'string' || !outputDirectory.trim()) {
      errors.push('Output directory must be a nonempty path when configured.');
    } else if (!path.isAbsolute(outputDirectory)) {
      errors.push('Output directory must be an absolute path.');
    } else {
      const normalizedPath = path.normalize(outputDirectory);
      try {
        if (!fs.statSync(normalizedPath).isDirectory()) {
          errors.push('Output directory must point to a directory.');
        } else {
          candidate.outputDirectory = normalizedPath;
        }
      } catch {
        errors.push('Output directory does not exist or cannot be accessed.');
      }
    }
  }

  return errors.length ? { errors } : { config: candidate, errors: [] };
}

export function loadRuntimeConfig(configPath: string): RuntimeConfigResult {
  try {
    const contents = fs.readFileSync(configPath, 'utf8');
    return validateRuntimeConfig(JSON.parse(contents) as unknown);
  } catch (error) {
    if ((error as { code?: string }).code === 'ENOENT') {
      return { errors: ['No saved runtime configuration was found.'] };
    }
    return {
      errors: [
        `Runtime configuration could not be read: ${
          error instanceof Error ? error.message : String(error)
        }`,
      ],
    };
  }
}

export function saveRuntimeConfig(
  configPath: string,
  config: RuntimeConfig,
): void {
  const validation = validateRuntimeConfig(config);
  if (!validation.config) {
    throw new Error(validation.errors.join('\n'));
  }

  fs.mkdirSync(path.dirname(configPath), { recursive: true });
  const temporaryPath = `${configPath}.${process.pid}.${Date.now()}.tmp`;
  try {
    fs.writeFileSync(
      temporaryPath,
      `${JSON.stringify(validation.config, null, 2)}\n`,
      { encoding: 'utf8', flag: 'wx', mode: 0o600 },
    );
    fs.renameSync(temporaryPath, configPath);
  } finally {
    if (fs.existsSync(temporaryPath)) fs.unlinkSync(temporaryPath);
  }
}

export function resolveAssetPath(root: string, requestUrl: string): string {
  const requestPath = decodeURIComponent(new URL(requestUrl).pathname);
  const relativePath = requestPath.replace(/^[/\\]+/, '');
  const resolvedRoot = path.resolve(root);
  const resolvedPath = path.resolve(resolvedRoot, relativePath);
  const pathFromRoot = path.relative(resolvedRoot, resolvedPath);

  if (
    !relativePath ||
    pathFromRoot.startsWith('..') ||
    path.isAbsolute(pathFromRoot)
  ) {
    throw new Error('Asset request is outside the configured root.');
  }

  return resolvedPath;
}
