import React, { useEffect, useState } from 'react';
import { IPC_CHANNEL } from '../../constants/channel';
import { DB_OPERATIONS } from '../../enums/db';
import { Filter } from '../components/Filter';
import { Loader, LoaderScreen } from '../components/Loader';
import { Interactive } from '../components/interactive';
import Drawer from '@mui/material/Drawer';

export interface CardProps {
  id: number;
  name: string;
  category: string;
  cardType: string;
  parent?: number | null;
  view: string | null;
}

export interface CardDetailsOwnProps {
  id: number;
}

export interface CardDetailsProps extends Interactive, CardDetailsOwnProps {}

export const CardDetails: React.FC<CardDetailsProps> = (
  props: CardDetailsProps,
) => {
  const { id, globalLabels } = props;
  const privateChannel = 'card-details';

  const [card, setCard] = useState<CardProps | undefined>(undefined);
  const [isDataLoading, setIsDataLoading] = useState(true);

  const [sidePanelContent, setSidePanelContent] = React.useState(<Loader />);
  const [sidePanelOpen, setSidePanelOpen] = React.useState(false);

  const toggleSidePanel = (newOpen: boolean) => () => {
    setSidePanelOpen(newOpen);
  };

  window.electron.ipcRenderer.once(privateChannel, (arg) => {
    console.log(`Data received: ${JSON.stringify(arg)}`);
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
            openSidePanel={() => toggleSidePanel(true)}
          />
        )}
      </div>
      <Drawer open={sidePanelOpen} onClose={toggleSidePanel(false)}>
        {sidePanelContent}
      </Drawer>
    </div>
  );
};
