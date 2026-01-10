export interface CategoryOwnProps {
   category?: string;
   id: number;
   name?: string;
   total?: number;
   subs: CategoryOwnProps[];
   searchTerm?: string;
   openCategories?: number[];
   chosenCategories?: {[key:number]: boolean}
 }
 
 export const satisfiesSearchTerm: (
   category: CategoryOwnProps,
   searchTerm?: string,
 ) => boolean = (category: CategoryOwnProps, searchTerm?: string) => {
   if (!searchTerm) {
     return true;
   }
   if (category.name?.toLowerCase().includes(searchTerm)) {
     return true;
   }
   return category.subs.some((sub) => satisfiesSearchTerm(sub, searchTerm));
 };