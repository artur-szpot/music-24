import Pagination from '@mui/material/Pagination';
import { useEffect, useState } from 'react';
import { MinionRow } from '../../constants/dbIpc';
import { LIMITS } from '../../constants/limits';
import { LoaderScreen } from '../components/Loader';
import { MinionInteractive } from '../components/Minion';
import { Interactive } from '../interfaces/interactive';
import { ScreenProps } from '../interfaces/screen';
import { navTo } from '../interfaces/setScreenProps';
import { MinionListOwnProps } from './MinionListProps';

export interface MinionListProps
  extends Interactive,
    MinionListOwnProps,
    ScreenProps {}

export const MinionList: React.FC<MinionListProps> = (
  props: MinionListProps,
) => {
  const { query, handleNav } = props;
  const [minions, setMinions] = useState<MinionRow[]>([]);
  const [page, setPage] = useState(0);
  const [itemTotal, setItemTotal] = useState(0);
  const [pageTotal, setPageTotal] = useState(1);
  const [isDataLoading, setIsDataLoading] = useState(true);
  const [isCountLoading, setIsCountLoading] = useState(true);
  const [listError, setListError] = useState('');
  const [countError, setCountError] = useState('');

  useEffect(() => {
    let active = true;
    setIsDataLoading(true);
    setListError('');
    window.electron.database
      .minions(query, page)
      .then((result) => {
        if (!active) return undefined;
        if (result.ok) {
          setMinions(result.data);
        } else {
          setListError(result.error.message);
        }
        setIsDataLoading(false);
        return undefined;
      })
      .catch(() => {
        if (active) {
          setListError('Could not load images.');
          setIsDataLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [query, page]);

  useEffect(() => {
    let active = true;
    setPage(0);
    setIsCountLoading(true);
    setCountError('');
    window.electron.database
      .minionCount(query)
      .then((result) => {
        if (!active) return undefined;
        if (result.ok) {
          setItemTotal(result.data);
          setPageTotal(Math.ceil(result.data / LIMITS.MINIONS_PER_PAGE));
        } else {
          setCountError(result.error.message);
        }
        setIsCountLoading(false);
        return undefined;
      })
      .catch(() => {
        if (active) {
          setCountError('Could not count images.');
          setIsCountLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [query]);

  if (isDataLoading || isCountLoading) {
    return <LoaderScreen />;
  }
  if (listError || countError)
    return (
      <div className="screen" role="alert">
        {listError || countError}
      </div>
    );

  return (
    <div className="screen">
      <div className="minion-screen-query">
        {query.cards && (
          <p>{`One of cards: ${query.cards.join(', ')} with relation "${query.rel}"`}</p>
        )}
        {query.episodes && (
          <p>{`One of episodes: ${query.episodes.join(', ')}`}</p>
        )}
        {query.seasons && (
          <p>{`One of seasons: ${query.seasons.join(', ')}`}</p>
        )}
        {query.scenes && <p>{`One of scenes: ${query.scenes.join(', ')}`}</p>}
        {query.ids && <p>{`One of IDs: ${query.ids.join(', ')}`}</p>}
        {query.view && <p>{`Coming from view: ${query.view}`}</p>}
      </div>
      <div className="minion-screen-contents">
        {!minions.length && <p>No images found.</p>}
        {minions.map((minion) => (
          <MinionInteractive
            {...minion}
            key={minion.id}
            onClick={() =>
              handleNav.setPopup(navTo.minionDetails({ id: minion.id }))
            }
          />
        ))}
      </div>
      <div className="screen-pagination">
        <p className="pagination-info">{`${itemTotal ? page * LIMITS.MINIONS_PER_PAGE + 1 : 0}-${Math.min((page + 1) * LIMITS.MINIONS_PER_PAGE, itemTotal)} of ${itemTotal}`}</p>
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
