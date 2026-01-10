import Pagination from '@mui/material/Pagination';
import { useEffect, useState } from 'react';
import { IPC_CHANNEL } from '../../constants/channel';
import { LIMITS } from '../../constants/limits';
import { DB_OPERATIONS } from '../../enums/db';
import { SCREENS } from '../../enums/screens';
import { LoaderScreen } from '../components/Loader';
import { MinionInteractive, MinionProps } from '../components/Minion';
import { Interactive } from '../interfaces/interactive';
import { MinionListOwnProps } from './MinionListProps';
import { ScreenProps } from '../interfaces/screen';

export interface MinionListProps extends Interactive, MinionListOwnProps, ScreenProps {}

export const MinionList: React.FC<MinionListProps> = (
  props: MinionListProps,
) => {
  const { query, handleNav } = props;
  const privateChannel = 'minions-list';
  const privateCountChannel = 'minions-list-count';
  const [minions, setMinions] = useState([] as MinionProps[]);
  const [page, setPage] = useState(-1);
  const [itemTotal, setItemTotal] = useState(0);
  const [pageTotal, setPageTotal] = useState(1);
  const [isDataLoading, setIsDataLoading] = useState(true);
  const [isCountLoading, setIsCountLoading] = useState(true);

  window.electron.ipcRenderer.once(privateChannel, (arg) => {
    setMinions(arg as MinionProps[]);
    setIsDataLoading(false);
  });

  window.electron.ipcRenderer.once(privateCountChannel, (arg) => {
    const totalItems = (arg as any)[0].total as number;
    const totalPages = Math.ceil(totalItems / LIMITS.MINIONS_PER_PAGE);
    setItemTotal(totalItems);
    setPageTotal(totalPages);
    setPage(0);
    setIsCountLoading(false);
  });

  useEffect(() => {
    window.electron.ipcRenderer.sendMessage(IPC_CHANNEL, {
      privateChannel,
      operation: DB_OPERATIONS.GET_MINIONS,
      query,
      page,
    });
  }, [query, page]);

  useEffect(() => {
    window.electron.ipcRenderer.sendMessage(IPC_CHANNEL, {
      privateChannel: privateCountChannel,
      operation: DB_OPERATIONS.GET_MINIONS_COUNT,
      query,
    });
  }, [query]);

  if (isDataLoading || isCountLoading) {
    return <LoaderScreen />;
  }

  return (
    <div className="screen">
      <div className="minion-screen-query">
        {query.cards && (
          <p>{`One of cards: ${query.cards.join(', ')} with relation "${query.rel}"`}</p>
        )}
        {query.episodes && (
          <p>{`One of episodes: ${query.episodes.join(', ')}`}</p>
        )}
        {query.scenes && <p>{`One of scenes: ${query.scenes.join(', ')}`}</p>}
        {query.ids && <p>{`One of IDs: ${query.ids.join(', ')}`}</p>}
        {query.view && <p>{`Coming from view: ${query.view}`}</p>}
      </div>
      <div className="minion-screen-contents">
        {minions.map((minion) => (
          <MinionInteractive
            {...minion}
            onClick={() =>
              handleNav.setPopup({
                screen: SCREENS.MINION_DETAILS,
                id: minion.id,
              })
            }
          />
        ))}
      </div>
      <div className="screen-pagination">
        <p className="pagination-info">{`${page * LIMITS.MINIONS_PER_PAGE + 1}-${Math.min((page + 1) * LIMITS.MINIONS_PER_PAGE, itemTotal)} of ${itemTotal}`}</p>
        <Pagination
          count={pageTotal}
          color="secondary"
          onChange={(event: React.ChangeEvent<unknown>, page: number) => {
            setPage(page - 1);
          }}
        />
      </div>
    </div>
  );
};
