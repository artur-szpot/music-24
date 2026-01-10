import Backdrop from '@mui/material/Backdrop';
import { useEffect, useState } from 'react';
import { IPC_CHANNEL } from '../constants/channel';
import { DB_OPERATIONS } from '../enums/db';
import { SCREEN_TYPES, SCREENS } from '../enums/screens';
import './App.css';
import { LoaderScreen } from './components/Loader';
import { GlobalLabels } from './globalLabels';
import { Nav } from './nav/Nav';
import { CardDetails } from './screens/CardDetails';
import { CategoryList } from './screens/CategoryList';
import { MinionDetails } from './screens/MinionDetails';
import { MinionList } from './screens/MinionList';
import { SetScreenProps } from './interfaces/setScreenProps';

export default function App() {
  const [screen, setScreen] = useState<SetScreenProps>({
    minionDetails: {
      id: 666
    },
    screenType: SCREEN_TYPES.SCREEN
  });
  const setPopup = (popup: SetScreenProps) => {
    setScreen({
      ...screen,
      popup: { ...popup, screenType: SCREEN_TYPES.POPUP },
    });
  };
  const [popupOpen, setPopupOpen] = useState(false);
  const handlePopupToggle = (newOpen: boolean) => {
    setPopupOpen(newOpen);
  };
  
  const handleNav = { handleNav: { setScreen, setPopup } };
  useEffect(() => {
    if (screen.popup !== undefined && !popupOpen) {
      handlePopupToggle(true);
    }
  }, [screen.popup]);

  const privateChannel = `app`;

  const [globalLabels, setGlobalLabels] = useState({} as GlobalLabels);
  const [isDataLoading, setIsDataLoading] = useState(true);

  window.electron.ipcRenderer.once(privateChannel, (response) => {
    const globalLabelsRaw: GlobalLabels = {
      cards: {},
      episodes: {},
      scenes: {},
      seasons: {
        0: 'Other',
        ...Object.fromEntries(
          Array.from({ length: 9 }).map((_, index) => [
            index + 1,
            `Season ${index + 1}`,
          ]),
        ),
      },
    };
    const typedResponse = response as {
      id: number;
      name: string;
      category: 'card' | 'scene' | 'episode';
    }[];

    typedResponse.forEach(({ id, name, category }) => {
      switch (category) {
        case 'card':
          globalLabelsRaw.cards[id] = name;
          break;
        case 'scene':
          globalLabelsRaw.scenes[id] = name;
          break;
        case 'episode':
          globalLabelsRaw.episodes[id] = name;
          break;
      }
    });

    setGlobalLabels(globalLabelsRaw);
    setIsDataLoading(false);
  });

  useEffect(() => {
    window.electron.ipcRenderer.sendMessage(IPC_CHANNEL, {
      privateChannel,
      operation: DB_OPERATIONS.INITIALIZE_LABELS,
    });
  }, []);

  if (isDataLoading) {
    return <LoaderScreen />;
  }

  const screenRenderer = (selectedScreen?: SetScreenProps) => {
   const { cardDetails, categoryList, minionDetails, minionList, screenType}=selectedScreen
   const screensSelected = [cardDetails,categoryList,minionDetails, minionList].filter(Boolean).length
   if(screensSelected !== 1){
      throw new Error(`Wrong number of screens selected. Expected 1, got ${screensSelected}`)
   }
   const commonProps = {
      ...handleNav,
      globalLabels,
      screenType,
   }
if(minionList){
        return (
          <MinionList
          {...minionList}
          {...commonProps}
          />
        );
}
      if(categoryList){
        return (
          <CategoryList
          {...categoryList}
          {...commonProps}
          />
        );
  }
      if(minionDetails){
        return (
          <MinionDetails
          {...minionDetails}
          {...commonProps}
          />
        );
      }
      if(cardDetails){
        return (
          <CardDetails
          {...cardDetails}
          {...commonProps}
          />
        );
    }
  };

  return (
    <div>
      <Nav handleNav={setScreen} />
      {screenRenderer(screen)}
      <Backdrop open={popupOpen}>
        <Backdrop open={true}>
          <Backdrop open={true} onClick={handlePopupToggle}>
            {screenRenderer(screen.popup)}
          </Backdrop>
        </Backdrop>
      </Backdrop>
    </div>
  );
}
