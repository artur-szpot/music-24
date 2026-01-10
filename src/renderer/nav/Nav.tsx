import { DB_OPERATIONS } from '../../enums/db';
import { SCREENS } from '../../enums/screens';
import { CategoryOwnProps } from '../components/Category';
import { SetScreenProps } from '../interfaces/setScreenProps';

export function Nav(props: { handleNav: (props: SetScreenProps) => void }) {
  const { handleNav } = props;
  return (
    <div id="nav">
      <button onClick={() => handleNav({ screen: SCREENS.HELLO })}>
        Test screen
      </button>
      <button
        onClick={() => handleNav({ screen: SCREENS.MINION_DETAILS, id: 1003 })}
      >
        Minion details
      </button>
      <button
        onClick={() => handleNav({ screen: SCREENS.CARD_DETAILS, id: 1038 })}
      >
        Card details
      </button>
      <button onClick={() => handleNav({ screen: SCREENS.MINIONS_LIST })}>
        Minion list
      </button>
      <button
        onClick={() =>
          handleNav({
            screen: SCREENS.CATEGORIES_LIST,
            dbOperation: DB_OPERATIONS.GET_TAG_CATEGORIES,
            searchTerm: undefined,
            actions: [
              {
                excludeTopCategories: true,
                text: (props: CategoryOwnProps) => `View ${props.total} images`,
                action: (props: CategoryOwnProps) =>
                  handleNav({
                    screen: SCREENS.MINIONS_LIST,
                    query: {
                      cards: [props.id!],
                      rel: 'p',
                    },
                  }),
              },
              { text: () => 'Edit subs', action: () => null, disabled: true },
            ],
          })
        }
      >
        Tags
      </button>
      <button
        onClick={() =>
          handleNav({
            screen: SCREENS.CATEGORIES_LIST,
            dbOperation: DB_OPERATIONS.GET_EPISODES,
            searchTerm: undefined,
            actions: [
              {
                excludeTopCategories: true,
                text: (props: CategoryOwnProps) => `View ${props.total} images`,
                action: (props: CategoryOwnProps) =>
                  handleNav({
                    screen: SCREENS.MINIONS_LIST,
                    query: {
                      episodes: [props.id!],
                    },
                  }),
              },
              {
                text: () => 'Show scenes?',
                action: () => null,
                disabled: true,
              },
            ],
          })
        }
      >
        Episodes
      </button>
      <button
        onClick={() =>
          handleNav({
            screen: SCREENS.CATEGORIES_LIST,
            dbOperation: DB_OPERATIONS.GET_SCENES,
            searchTerm: undefined,
            actions: [
              {
                excludeTopCategories: true,
                text: (props: CategoryOwnProps) => `View ${props.total} images`,
                action: (props: CategoryOwnProps) =>
                  handleNav({
                    screen: SCREENS.MINIONS_LIST,
                    query: {
                      ...(props.id! < 0 && { episodes: [-props.id!] }),
                      ...(props.id! >= 0 && { scenes: [props.id!] }),
                    },
                  }),
              },
            ],
          })
        }
      >
        Scenes
      </button>
      <button
        onClick={() =>
          handleNav({
            screen: SCREENS.CATEGORIES_LIST,
            dbOperation: DB_OPERATIONS.GET_IMPLEMENTATION_CATEGORIES,
          })
        }
      >
        Card implementations
      </button>
    </div>
  );
}
