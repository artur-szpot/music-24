import { SetScreenProps } from '../interfaces/setScreenProps';
import { CategoryBasicProps } from './CategoryProps';

export interface CategoryAction<T> {
  excludeTopCategories?: boolean;
  text: (props: CategoryBasicProps) => string;
  action: T;
  disabled?: boolean;
}

export interface CategoryActionProps {
  actions?: CategoryAction<(props: CategoryBasicProps) => void>[];
  navActions?: CategoryAction<(props: CategoryBasicProps) => SetScreenProps>[];
}
