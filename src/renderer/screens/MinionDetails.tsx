import React, { useEffect, useState } from 'react';
import { IPC_CHANNEL } from '../../constants/channel';
import { DB_OPERATIONS } from '../../enums/db';
import { LoaderScreen } from '../components/Loader';
import { Minion, MinionOwnProps } from '../components/Minion';

export interface MinionDetailsOwnProps {
  id: number;
  popup?: boolean;
}

export interface MinionDetailsProps extends MinionDetailsOwnProps {}

export const MinionDetails: React.FC<MinionDetailsProps> = (
  props: MinionDetailsProps,
) => {
  const { id, popup } = props;
  const privateChannel = 'minion-details';

  const [minion, setMinion] = useState<MinionOwnProps | undefined>(undefined);
  const [isDataLoading, setIsDataLoading] = useState(true);

  window.electron.ipcRenderer.once(privateChannel, (arg) => {
    console.log(`Data received: ${JSON.stringify(arg)}`);
    setMinion({ ...(arg as MinionOwnProps[])[0] });
    setIsDataLoading(false);
  });

  useEffect(() => {
    window.electron.ipcRenderer.sendMessage(IPC_CHANNEL, {
      privateChannel,
      operation: DB_OPERATIONS.GET_MINIONS,
      query: { ids: [id] },
    });
  }, [id]);

  if (isDataLoading || !minion) {
    return <LoaderScreen />;
  }

  return (
    <div className={popup ? 'screen-popup' : 'screen'}>
      <div className="minion-screen-contents">
        <Minion {...minion} fullSize={true} />
      </div>
    </div>
  );
};
