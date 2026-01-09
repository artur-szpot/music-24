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
import { CategoriesList } from './screens/CategoriesList';
import { Hello } from './screens/Hello';
import { MinionDetails } from './screens/MinionDetails';
import { MinionsList } from './screens/MinionsList';
import { SetScreenProps } from './setScreenProps';

export default function App() {
  const [screen, setScreen] = useState<SetScreenProps>({
    screen: SCREENS.HELLO,
  });
  const setPopup = (popup: SetScreenProps) => {
    setScreen({
      ...screen,
      popup: { ...popup, screenType: SCREEN_TYPES.POPUP },
    });
  };
  const [popupOpen, setPopupOpen] = useState(false);
  const handleClose = () => {
    setPopupOpen(false);
  };
  const handleOpen = () => {
    setPopupOpen(true);
  };
  const handleNav = { handleNav: { setScreen, setPopup } };

  useEffect(() => {
    if (screen.popup !== undefined && !popupOpen) {
      handleOpen();
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
    switch (selectedScreen?.screen) {
      default:
        return <Hello />;
      case SCREENS.MINIONS_LIST:
        return (
          <MinionsList
            {...handleNav}
            globalLabels={globalLabels}
            query={selectedScreen.query ?? { cards: [666] }}
          />
        );
      case SCREENS.CATEGORIES_LIST:
        return (
          <CategoriesList
            {...handleNav}
            globalLabels={globalLabels}
            dbOperation={selectedScreen.dbOperation ?? DB_OPERATIONS.GET_MINION}
            searchTerm={selectedScreen.searchTerm}
            actions={selectedScreen.actions ?? []}
          />
        );
      case SCREENS.MINION_DETAILS:
        return (
          <MinionDetails
            id={selectedScreen.id ?? 666}
            screenType={selectedScreen.screenType ?? SCREEN_TYPES.SCREEN}
          />
        );
      case SCREENS.CARD_DETAILS:
        return (
          <CardDetails
            {...handleNav}
            globalLabels={globalLabels}
            id={selectedScreen.id ?? 666}
          />
        );
    }
  };

  return (
    <div>
      <Nav handleNav={setScreen} />
      {screenRenderer(screen)}
      <Backdrop open={popupOpen} onClick={handleClose}>
        <Backdrop open={true} onClick={handleClose}>
          <Backdrop open={true} onClick={handleClose}>
            {screenRenderer(screen.popup)}
          </Backdrop>
        </Backdrop>
      </Backdrop>
    </div>
  );
}
