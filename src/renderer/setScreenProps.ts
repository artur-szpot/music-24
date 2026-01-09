import { DB_OPERATIONS } from '../enums/db';
import { SCREEN_TYPES, SCREENS } from '../enums/screens';
import { CategoryAction } from './components/Category';
import { MinionsListQuery } from './screens/MinionsList';

export interface SetScreenProps {
  screen: SCREENS;
  dbOperation?: DB_OPERATIONS;
  query?: MinionsListQuery;
  searchTerm?: string;
  popup?: SetScreenProps;
  id?: number;
  actions?: CategoryAction[];
  screenType?: SCREEN_TYPES;
}
