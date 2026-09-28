import { MinionQuery } from '../../constants/dbIpc';

export type MinionListQuery = MinionQuery;

export interface MinionListOwnProps {
  query: MinionListQuery;
}
