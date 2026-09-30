import Alert from '@mui/material/Alert';
import CssBaseline from '@mui/material/CssBaseline';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import { ThemeProvider } from '@mui/material/styles';
import { useEffect, useState } from 'react';
import { SCREEN_TYPES } from '../enums/screens';
import './App.css';
import { LoaderScreen } from './components/Loader';
import { GlobalLabels } from './globalLabels';
import { Nav } from './nav/Nav';
import { CardDetails } from './screens/CardDetails';
import { CategoryList } from './screens/CategoryList';
import { MinionDetails } from './screens/MinionDetails';
import { MinionList } from './screens/MinionList';
import Settings from './screens/Settings';
import theme from './theme';
import {
  placeholderScreenProps,
  SetScreenProps,
} from './interfaces/setScreenProps';

function AppContent() {
  const [screen, setScreen] = useState<SetScreenProps>(placeholderScreenProps);
  const [settingsOpen, setSettingsOpen] = useState(false);
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

  const [globalLabels, setGlobalLabels] = useState({} as GlobalLabels);
  const [isDataLoading, setIsDataLoading] = useState(true);
  const [labelsError, setLabelsError] = useState('');

  useEffect(() => {
    let active = true;
    window.electron.database
      .labels()
      .then((result) => {
        if (!active) return undefined;
        if (!result.ok) {
          setLabelsError(result.error.message);
        } else {
          const labels: GlobalLabels = {
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
          result.data.forEach(({ id, name, category }) => {
            if (category === 'card') labels.cards[id] = name;
            if (category === 'scene') labels.scenes[id] = name;
            if (category === 'episode') labels.episodes[id] = name;
          });
          setGlobalLabels(labels);
        }
        setIsDataLoading(false);
        return undefined;
      })
      .catch(() => {
        if (active) {
          setLabelsError('Could not load labels.');
          setIsDataLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, []);

  if (isDataLoading) {
    return <LoaderScreen />;
  }

  const screenRenderer = (selectedScreen: SetScreenProps) => {
    const {
      cardDetails,
      categoryList,
      minionDetails,
      minionList,
      screenType = SCREEN_TYPES.SCREEN,
    } = selectedScreen ?? {};
    const screensSelected = [
      cardDetails,
      categoryList,
      minionDetails,
      minionList,
    ].filter((screen) => screen !== undefined).length;
    if (screensSelected !== 1) {
      throw new Error(
        `Wrong number of screens selected. Expected 1, got ${screensSelected}`,
      );
    }
    const commonProps = {
      ...handleNav,
      globalLabels,
      screenType,
    };
    if (minionList) {
      return <MinionList {...minionList} {...commonProps} />;
    }
    if (categoryList) {
      return <CategoryList {...categoryList} {...commonProps} />;
    }
    if (minionDetails) {
      return <MinionDetails {...minionDetails} {...commonProps} />;
    }
    if (cardDetails) {
      return <CardDetails {...cardDetails} {...commonProps} />;
    }
  };

  return (
    <div className="app-shell">
      <Nav
        handleNav={(next) => {
          setSettingsOpen(false);
          setScreen(next);
        }}
        onSettings={() => {
          setPopupOpen(false);
          setSettingsOpen(true);
        }}
      />
      <div className="app-content">
        {settingsOpen && <Settings onClose={() => setSettingsOpen(false)} />}
        {!settingsOpen && labelsError && (
          <main className="screen">
            <Alert severity="error" role="alert">
              {labelsError}
            </Alert>
          </main>
        )}
        {!settingsOpen && !labelsError && screenRenderer(screen)}
      </div>
      {!settingsOpen && !labelsError && (
        <Dialog
          open={popupOpen}
          onClose={() => handlePopupToggle(false)}
          maxWidth="xl"
          fullWidth
          scroll="paper"
        >
          <DialogContent sx={{ p: 0 }}>
            {screenRenderer(screen.popup ?? placeholderScreenProps)}
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppContent />
    </ThemeProvider>
  );
}
