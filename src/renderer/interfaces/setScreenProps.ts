import { SCREEN_TYPES } from '../../enums/screens';
import { CategoryActionProps } from '../components/CategoryActionProps';
import {
  CategoryBasicProps,
  CategoryOwnProps,
} from '../components/CategoryProps';
import { CardDetailsOwnProps } from '../screens/CardDetailsProps';
import { CategoryListOwnProps } from '../screens/CategoryListProps';
import { MinionDetailsOwnProps } from '../screens/MinionDetailsProps';
import {
  MinionListOwnProps,
  MinionListQuery,
} from '../screens/MinionListProps';

export interface SetScreenProps {
  cardDetails?: CardDetailsOwnProps;
  categoryList?: CategoryListOwnProps & CategoryActionProps;
  minionDetails?: MinionDetailsOwnProps;
  minionList?: MinionListOwnProps;
  popup?: SetScreenProps;
  screenType: SCREEN_TYPES;
}

export const placeholderScreenProps: SetScreenProps = {
  minionDetails: {
    id: 666,
  },
  screenType: SCREEN_TYPES.SCREEN,
};

interface NavToCommon {
  screenType?: SCREEN_TYPES;
}

interface NavTo {
  cardDetails: (args: { id: number } & NavToCommon) => SetScreenProps;
  tagsList: (args: { searchTerm?: string } & NavToCommon) => SetScreenProps;
  cardImplementationsList: (
    args: { searchTerm?: string } & NavToCommon,
  ) => SetScreenProps;
  scenesList: (args: { searchTerm?: string } & NavToCommon) => SetScreenProps;
  minionDetails: (args: { id: number } & NavToCommon) => SetScreenProps;
  minionList: (
    args: { query: MinionListQuery } & NavToCommon,
  ) => SetScreenProps;
}

export const navTo: NavTo = {
  cardDetails: ({ id, screenType }) => ({
    cardDetails: { id },
    screenType: screenType ?? SCREEN_TYPES.SCREEN,
  }),
  tagsList: ({ searchTerm, screenType }) => ({
    categoryList: {
      dbOperation: 'tags',
      searchTerm,
      navActions: [
        {
          excludeTopCategories: true,
          text: (props: CategoryBasicProps) => `View ${props.total} images`,
          action: (props: CategoryBasicProps) =>
            navTo.minionList({
              query: {
                cards: [props.id!],
                rel: 'p',
              },
            }),
        },
        {
          text: () => 'Edit subs',
          action: () => navTo.tagsList({}),
          disabled: true,
        },
      ],
    },
    screenType: screenType ?? SCREEN_TYPES.SCREEN,
  }),
  cardImplementationsList: ({ searchTerm, screenType }) => ({
    categoryList: {
      dbOperation: 'implementations',
      searchTerm,
      actions: [],
    },
    screenType: screenType ?? SCREEN_TYPES.SCREEN,
  }),
  scenesList: ({ searchTerm, screenType }) => ({
    categoryList: {
      dbOperation: 'scenes',
      searchTerm,
      navActions: [
        {
          excludeTopCategories: true,
          text: (props: CategoryBasicProps) => `View ${props.total} images`,
          action: (props: CategoryBasicProps) =>
            navTo.minionList({
              query: {
                ...(props.id! < 0 && { episodes: [-props.id!] }),
                ...(props.id! >= 0 && { scenes: [props.id!] }),
              },
            }),
        },
      ],
    },
    screenType: screenType ?? SCREEN_TYPES.SCREEN,
  }),
  minionDetails: ({ id, screenType }) => ({
    minionDetails: { id },
    screenType: screenType ?? SCREEN_TYPES.SCREEN,
  }),
  minionList: ({ query, screenType }) => ({
    minionList: { query },
    screenType: screenType ?? SCREEN_TYPES.SCREEN,
  }),
};
