import React, { useEffect, useState } from 'react';
import { IPC_CHANNEL } from '../../constants/channel';
import { DB_OPERATIONS } from '../../enums/db';
import { Filter } from '../components/Filter';
import { LoaderScreen } from '../components/Loader';
import { Interactive } from '../interfaces/interactive';
import Drawer from '@mui/material/Drawer';
import { MinionDetails } from './MinionDetails';
import { SCREEN_TYPES } from '../../enums/screens';
import { CardProps } from '../interfaces/card';
import { CardDetailsOwnProps } from './CardDetailsProps';
import { ScreenProps } from '../interfaces/screen';

export interface CardDetailsProps extends Interactive, CardDetailsOwnProps, ScreenProps {}

export const CardDetails: React.FC<CardDetailsProps> = (
  props: CardDetailsProps,
) => {
  const { id, globalLabels } = props;
  const privateChannel = 'card-details';

  const [card, setCard] = useState<CardProps | undefined>(undefined);
  const [isDataLoading, setIsDataLoading] = useState(true);

  const [sidePanelContent, setSidePanelContent] = React.useState(
    <MinionDetails id={666} screenType={SCREEN_TYPES.SIDE_PANEL} />,
  );
  const [sidePanelOpen, setSidePanelOpen] = React.useState(true);

  const toggleSidePanel = (newOpen: boolean) => {
    setSidePanelOpen(newOpen);
  };

  window.electron.ipcRenderer.once(privateChannel, (arg) => {
    setCard((arg as CardProps[])[0]);
    setIsDataLoading(false);
  });

  useEffect(() => {
    window.electron.ipcRenderer.sendMessage(IPC_CHANNEL, {
      privateChannel,
      operation: DB_OPERATIONS.GET_CARDS,
      query: { ids: [id] },
    });
  }, [id]);

  if (isDataLoading || !card) {
    return <LoaderScreen />;
  }

  const { name, category, view: viewRaw } = card;
  const view = JSON.parse(viewRaw ?? '');

  return (
    <div className="screen card-details-screen">
      <div className="card-screen-contents">
        <h1>{name} </h1>
        <p>{`Category: ${category}`}</p>
        {view && (
          <Filter
            {...view}
            globalLabels={globalLabels}
            openSidePanel={toggleSidePanel}
          />
        )}
      </div>
      <Drawer
        open={sidePanelOpen}
        anchor="right"
        onClose={() => toggleSidePanel(false)}
      >
        {sidePanelContent}
      </Drawer>
    </div>
  );
};
