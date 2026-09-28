import React, { useEffect, useState } from 'react';
import { Filter } from '../components/Filter';
import { LoaderScreen } from '../components/Loader';
import { Interactive } from '../interfaces/interactive';
import Drawer from '@mui/material/Drawer';
import { MinionDetails } from './MinionDetails';
import { SCREEN_TYPES } from '../../enums/screens';
import { CardProps } from '../interfaces/card';
import { CardDetailsOwnProps } from './CardDetailsProps';
import { ScreenProps } from '../interfaces/screen';

export interface CardDetailsProps
  extends Interactive,
    CardDetailsOwnProps,
    ScreenProps {}

export const CardDetails: React.FC<CardDetailsProps> = (
  props: CardDetailsProps,
) => {
  const { id, globalLabels } = props;
  const [card, setCard] = useState<CardProps | undefined>(undefined);
  const [isDataLoading, setIsDataLoading] = useState(true);
  const [error, setError] = useState('');

  const [sidePanelContent, setSidePanelContent] = React.useState(
    <MinionDetails id={666} screenType={SCREEN_TYPES.SIDE_PANEL} />,
  );
  const [sidePanelOpen, setSidePanelOpen] = React.useState(true);

  const toggleSidePanel = (newOpen: boolean) => {
    setSidePanelOpen(newOpen);
  };

  useEffect(() => {
    let active = true;
    setIsDataLoading(true);
    window.electron.database
      .cards([id])
      .then((result) => {
        if (!active) return undefined;
        if (result.ok) {
          setCard(result.data[0]);
          setError(result.data.length ? '' : 'Card not found.');
        } else {
          setError(result.error.message);
        }
        setIsDataLoading(false);
        return undefined;
      })
      .catch(() => {
        if (active) {
          setError('Could not load card.');
          setIsDataLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [id]);

  if (isDataLoading) {
    return <LoaderScreen />;
  }
  if (error || !card)
    return (
      <div className="screen" role="alert">
        {error || 'Card not found.'}
      </div>
    );

  const { name, category, view: viewRaw } = card;
  const view = viewRaw ? JSON.parse(viewRaw) : null;

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
