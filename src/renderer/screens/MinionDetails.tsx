import React, { useEffect, useState } from 'react';
import { IPC_CHANNEL } from '../../constants/channel';
import { DB_OPERATIONS } from '../../enums/db';
import { LoaderScreen } from '../components/Loader';
import { Minion, MINION_SIZES, MinionOwnProps } from '../components/Minion';
import { SCREEN_TYPES } from '../../enums/screens';

export interface MinionDetailsOwnProps {
  id: number;
  screenType: SCREEN_TYPES;
}

export interface MinionDetailsProps extends MinionDetailsOwnProps {}

export const MinionDetails: React.FC<MinionDetailsProps> = (
  props: MinionDetailsProps,
) => {
  const { id, screenType } = props;
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

  const size = ((_screenType: SCREEN_TYPES) => {
    switch (_screenType) {
      case SCREEN_TYPES.SCREEN:
      case SCREEN_TYPES.POPUP:
        return MINION_SIZES.SOLO;
      case SCREEN_TYPES.SIDE_PANEL:
      case SCREEN_TYPES.TOOLTIP:
        return MINION_SIZES.FULL;
      default:
        throw new Error(`Screen type not covered: ${_screenType}`);
    }
  })(screenType);

  switch (size) {
    case MINION_SIZES.SOLO:
      return (
        <div className={screenType}>
          <div className="minion-screen-contents">
            <Minion {...minion} size={size} />
          </div>
        </div>
      );
    default:
      return (
        <div className={screenType}>
          <Minion {...minion} size={size} />
        </div>
      );
  }
};
