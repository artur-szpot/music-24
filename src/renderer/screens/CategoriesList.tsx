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
import { Interactive } from '../components/interactive';
import { LoaderScreen } from '../components/Loader';

export interface CategoriesListOwnProps {
  dbOperation: DB_OPERATIONS;
  searchTerm?: string;
  actions: CategoryAction[];
}

export interface CategoriesListProps
  extends Interactive,
    CategoriesListOwnProps {}

export const CategoriesList: React.FC<CategoriesListProps> = (
  props: CategoriesListProps,
) => {
  const { dbOperation, handleNav, globalLabels } = props;
  const privateChannel = `categories-list-${dbOperation}`;

  const [categories, setCategories] = useState([] as CategoryOwnProps[]);
  const [openCategory, setOpenCategory] = useState<string | undefined>(
    undefined,
  );
  const handleOpenCategory =
    (category: string) =>
    (event: React.SyntheticEvent, newExpanded: boolean) => {
      setOpenCategory(newExpanded ? category : undefined);
    };
  const [searchTerm, setSearchTerm] = useState<string | undefined>(
    props.searchTerm,
  );
  const handleSearch = (value: string) => {
    value.length ? setSearchTerm(value) : setSearchTerm(undefined);
  };
  const [isDataLoading, setIsDataLoading] = useState(true);

  window.electron.ipcRenderer.once(privateChannel, (response) => {
    console.log(`Data received: ${JSON.stringify(response)}`);

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
        try {
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
        } catch (e) {
          alert(e);
          alert(Object.values(categoryMap).length);
        }
      });

    setCategories(Object.values(categoryMap));
    setIsDataLoading(false);
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

  return (
    <div className="screen accordion-screen">
      <TextField
        autoFocus
        onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
          handleSearch(event.target.value)
        }
        fullWidth
      />
      <div className="spacer"></div>
      {categories
        .filter((category) => satisfiesSearchTerm(category, searchTerm))
        .map((category) => (
          <Category
            {...category}
            searchTerm={searchTerm}
            key={category.name}
            handleNav={handleNav}
            globalLabels={globalLabels}
            expanded={searchTerm ? true : category.name === openCategory}
            onChange={handleOpenCategory(category.name ?? '')}
            actions={props.actions}
            topCategory={true}
          />
        ))}
    </div>
  );
};
