import { CategoryKind } from '../../constants/dbIpc';

export interface CategoryListOwnProps {
  dbOperation: CategoryKind;
  searchTerm?: string;
  openCategories?: number[];
  chosenCategories?: { [key: number]: boolean };
}
