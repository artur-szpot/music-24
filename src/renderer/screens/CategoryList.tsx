import TextField from '@mui/material/TextField';
import { useEffect, useState } from 'react';
import { CategoryRow } from '../../constants/dbIpc';
import { Category } from '../components/Category';
import { CategoryActionProps } from '../components/CategoryActionProps';
import {
  CategoryOwnProps,
  satisfiesSearchTerm,
} from '../components/CategoryProps';
import { LoaderScreen } from '../components/Loader';
import { Interactive } from '../interfaces/interactive';
import { ScreenProps } from '../interfaces/screen';
import { CategoryListOwnProps } from './CategoryListProps';

export interface CategoryListProps
  extends Interactive,
    CategoryListOwnProps,
    ScreenProps,
    CategoryActionProps {}

export const CategoryList: React.FC<CategoryListProps> = ({
  dbOperation,
  handleNav,
  globalLabels,
  actions,
  navActions,
  chosenCategories: chosenCategoriesProps = {},
  openCategories: openCategoriesProps = [],
  searchTerm: searchTermProps,
}: CategoryListProps) => {
  useState<number[]>(openCategoriesProps);
  const [openCategory, setOpenCategory] = useState<number | undefined>(
    undefined,
  );
  const [openCategories, setOpenCategories] =
    useState<number[]>(openCategoriesProps);
  const handleOpenCategory = (args: {
    add?: number | undefined;
    remove?: number | undefined;
  }) => {
    const newOpenCategories = [...openCategories, args.add].filter(
      (category) => ![undefined, args.remove].includes(category),
    ) as number[];
    setOpenCategories(newOpenCategories);
    setOpenCategory(
      newOpenCategories.find((category) =>
        categories.map((cat) => cat.id).includes(category),
      ),
    );
  };

  const [chosenCategories, setChosenCategories] = useState<{
    [key: number]: boolean;
  }>(chosenCategoriesProps);
  const handleChosenCategory = (id: number) => {
    const newChosenCategories = { ...chosenCategories };
    const currentState = newChosenCategories[id];
    switch (currentState) {
      case undefined:
        newChosenCategories[id] = true;
        break;
      case true:
        newChosenCategories[id] = false;
        break;
      case false:
        delete newChosenCategories[id];
    }
    setChosenCategories(newChosenCategories);
  };

  const [searchTerm, setSearchTerm] = useState<string | undefined>(
    searchTermProps,
  );
  const handleSearch = (value: string) => {
    value.length ? setSearchTerm(value) : setSearchTerm(undefined);
  };
  const onSearchChange = (event: React.ChangeEvent<HTMLInputElement>) =>
    handleSearch(event.target.value);

  const [categories, setCategories] = useState([] as CategoryOwnProps[]);
  const [isDataLoading, setIsDataLoading] = useState(true);
  const [error, setError] = useState('');
  const openCategoryIds = openCategoriesProps.join(',');

  useEffect(() => {
    let active = true;
    setIsDataLoading(true);
    window.electron.database
      .categories(dbOperation)
      .then((result) => {
        if (!active) return undefined;
        if (!result.ok) {
          setError(result.error.message);
        } else {
          const categoryMap: Record<string, CategoryOwnProps> = {};
          const subs: CategoryRow[] = result.data;
          const processSubs = (targetParent: number): CategoryOwnProps[] =>
            subs
              .filter(({ parent }) => parent === targetParent)
              .map((sub) => ({ ...sub, subs: processSubs(sub.id) }));
          subs
            .filter(({ parent }) => parent === null)
            .forEach((sub) => {
              if (categoryMap[sub.category] === undefined) {
                categoryMap[sub.category] = {
                  id: -Object.values(categoryMap).length,
                  name: sub.category,
                  subs: [],
                };
              }
              categoryMap[sub.category].subs.push({
                ...sub,
                subs: processSubs(sub.id),
              });
            });
          const parsedCategories = Object.values(categoryMap);
          setCategories(parsedCategories);
          setOpenCategory(
            parsedCategories.find((category) =>
              openCategoryIds.split(',').includes(String(category.id)),
            )?.id,
          );
          setError('');
        }
        setIsDataLoading(false);
        return undefined;
      })
      .catch(() => {
        if (active) {
          setError('Could not load categories.');
          setIsDataLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [dbOperation, openCategoryIds]);

  if (isDataLoading) {
    return <LoaderScreen />;
  }

  if (error)
    return (
      <div className="screen" role="alert">
        {error}
      </div>
    );

  const passableProps = {
    searchTerm,
    handleNav,
    globalLabels,
    handleOpenCategory,
    handleChosenCategory,
    actions,
    navActions,
  };

  return (
    <div className="screen accordion-screen">
      <TextField autoFocus onChange={onSearchChange} fullWidth />
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
