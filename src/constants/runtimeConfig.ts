export interface RuntimeConfig {
  databasePath: string;
  minionRoot: string;
  cardRoot: string;
  fileSystemRoot: string;
}

export type RuntimeConfigKey = keyof RuntimeConfig;

export interface ConfigUpdateResult {
  restarting: boolean;
  errors: string[];
}

export const CONFIG_CHANNELS = {
  GET: 'config:get',
  CHOOSE: 'config:choose',
  APPLY: 'config:apply',
} as const;
