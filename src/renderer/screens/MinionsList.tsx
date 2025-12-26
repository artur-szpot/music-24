import { useCallback, useEffect, useState } from 'react';
import { DB_OPERATIONS } from '../../enums/db';
import { Minion, MinionProps } from '../components/Minion';
import { CHANNELS } from '../../enums/channels';
import { LIMITS } from '../../constants/limits';

export interface MinionsListProps {
  episodes?: number[];
}

export const MinionsList: React.FC<MinionsListProps> = (
  props: MinionsListProps,
) => {
  const { episodes } = props;
  const [minions, setMinions] = useState([] as MinionProps[]);
  const [page, setPage] = useState(-1);
  const [itemTotal, setItemTotal] = useState(0);
  const [pageTotal, setPageTotal] = useState(1);
  const [isDataLoading, setIsDataLoading] = useState(true);
  const [isCountLoading, setIsCountLoading] = useState(true);

  window.electron.ipcRenderer.once(CHANNELS.DEFAULT, (arg) => {
    console.log(`Data received: ${JSON.stringify(arg)}`);
    setMinions(arg as MinionProps[]);
    setIsDataLoading(false);
  });

  window.electron.ipcRenderer.once(CHANNELS.COUNT, (arg) => {
    console.log(`Count received: ${JSON.stringify(arg)}`);
    const totalItems = (arg as any)[0]['count(1)'] as number;
    const totalPages = Math.ceil(totalItems / LIMITS.MINIONS_PER_PAGE);
    setItemTotal(totalItems);
    setPageTotal(totalPages);
    setPage(0);
    setIsCountLoading(false);
  });

  useEffect(() => {
    window.electron.ipcRenderer.sendMessage(CHANNELS.DEFAULT, {
      operation: DB_OPERATIONS.GET_MINIONS,
      episodes,
      page,
    });
  }, [episodes, page]);

  useEffect(() => {
    window.electron.ipcRenderer.sendMessage(CHANNELS.COUNT, {
      operation: DB_OPERATIONS.GET_MINIONS_COUNT,
      episodes,
    });
  }, [episodes]);

  if (isDataLoading || isCountLoading) {
    return (
      <div className="screen">
        <p className="loading">Loading...</p>
      </div>
    );
  }

  return (
    <div className="screen">
      <div className="screen-contents">
        {minions.map((minion) => (
          <Minion {...minion} />
        ))}
      </div>
      <div className="screen-pagination">
        <p>{`Page ${page + 1} of ${pageTotal} (showing items ${page * LIMITS.MINIONS_PER_PAGE + 1}-${(page + 1) * LIMITS.MINIONS_PER_PAGE} of ${itemTotal})`}</p>
      </div>
    </div>
  );
};
