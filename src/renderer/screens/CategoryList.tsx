import TextField from '@mui/material/TextField';
import { useEffect, useState } from 'react';
import { IPC_CHANNEL } from '../../constants/channel';
import { DB_OPERATIONS } from '../../enums/db';
import { SubCard } from '../../main/db';
import {
  Category,
  CategoryAction,
  CategoryOwnProps,
  satisfiesSearchTerm,
} from '../components/Category';
import { Interactive } from '../interfaces/interactive';
import { LoaderScreen } from '../components/Loader';
import { CategoryListOwnProps } from './CategoryListProps';
import { ScreenProps } from '../interfaces/screen';
import { CategoryActionProps } from '../components/CategoryActionProps';

export interface CategoryListProps
  extends Interactive,
    CategoryListOwnProps, ScreenProps, CategoryActionProps {}

export const CategoryList: React.FC<CategoryListProps> = (
   { dbOperation, handleNav, globalLabels, actions, navActions, chosenCategories:chosenCategoriesProps={}, openCategories: openCategoriesProps=[],searchTerm:searchTermProps }: CategoryListProps,
) => {
  const [openCategories, setOpenCategories] = useState<number[]>(
     openCategoriesProps
     );
     const handleOpenCategory =
     (args:{add?:number|undefined, remove?:number|undefined}) =>
      setOpenCategories([...openCategories, args.add].filter((category)=>![undefined, args.remove].includes( category)));
      
      const [chosenCategories, setChosenCategories] = useState<{[key:number]: boolean}>(chosenCategoriesProps);
      const handleChosenCategory =
    (id: number) =>{
      const newChosenCategories = {...chosenCategories}
      const currentState = newChosenCategories[id]
      switch(currentState){
         case undefined:
            newChosenCategories[id] = true
            break
            case true:
               newChosenCategories[id]=false
               break
               case false:
                  delete newChosenCategories[id]
      }
      setChosenCategories(newChosenCategories);
    }
  
  const [searchTerm, setSearchTerm] = useState<string | undefined>(
    searchTermProps,
  );
  const handleSearch = (value: string) => {
    value.length ? setSearchTerm(value) : setSearchTerm(undefined);
  };
  const onSearchChange = (event: React.ChangeEvent<HTMLInputElement>) =>
  handleSearch(event.target.value)

  const privateChannel = `categories-list-${dbOperation}`;
  const [categories, setCategories] = useState([] as CategoryOwnProps[]);
  const [isDataLoading, setIsDataLoading] = useState(true);

  window.electron.ipcRenderer.once(privateChannel, (response) => {
   try {
    const categoryMap = {} as { [key: string]: CategoryOwnProps };

    const subs = response as SubCard[];
    const processSubs: (targetParent: number) => CategoryOwnProps[] = (
      targetParent: number,
    ) =>
      subs
        .filter(({ parent }) => parent === targetParent)
        .map((sub) => ({ ...sub, handleNav, subs: processSubs(sub.id) }));
    subs
      .filter(({ parent }) => parent === null)
      .forEach((sub) => {
          if (categoryMap[sub.category] === undefined) {
            categoryMap[sub.category] = {
              id: sub.id,
              category: sub.category,
              name: sub.category,
              subs: [],
            };
          }
          categoryMap[sub.category].subs.push({
            ...sub,
            subs: processSubs(sub.id),
          });
      });

    setCategories(Object.values(categoryMap));
    setIsDataLoading(false);
   } catch (e) {
     alert(`Error encountered while loading data for CategoryList: ${e}`);
   }
  });

  useEffect(() => {
    window.electron.ipcRenderer.sendMessage(IPC_CHANNEL, {
      privateChannel,
      operation: dbOperation,
    });
  }, [dbOperation]);

  if (isDataLoading) {
    return <LoaderScreen />;
  }

  const passableProps = {
     searchTerm,
     handleNav,
     globalLabels,
     handleOpenCategory,
     handleChosenCategory,
     actions,
     navActions}
     

  return (
    <div className="screen accordion-screen">
      <TextField
        autoFocus
        onChange={onSearchChange        }
        fullWidth
      />
      <div className="spacer"></div>
      {categories
        .filter((category) => satisfiesSearchTerm(category, searchTerm))
        .map((category) => (
          <Category
            {...category}
            {...passableProps}
            key={category.name}
            expanded={searchTerm ? true : category.id === openCategory}
            topCategory={true}
          />
        ))}
    </div>
  );
};
