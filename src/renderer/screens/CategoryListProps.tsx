import { DB_OPERATIONS } from '../../enums/db';

export interface CategoryListOwnProps {
  dbOperation: DB_OPERATIONS;
  searchTerm?: string;
  openCategories?: number[];
  chosenCategories?: { [key: number]: boolean };
}
