import { SetScreenProps } from "../interfaces/setScreenProps";
import { CategoryOwnProps } from "./CategoryProps";

 export interface CategoryAction<T> {
   excludeTopCategories?: boolean;
   text: (props: CategoryOwnProps) => string;
   action: T;
   disabled?: boolean;
 }
 
 export interface CategoryActionProps {
   actions: CategoryAction<(props: CategoryOwnProps) => void>[];
   navActions: CategoryAction<(props: CategoryOwnProps) => SetScreenProps>[];
 }