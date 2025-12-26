import { useState } from 'react';
import { SCREENS } from '../enums/screens';
import './App.css';
import { Nav } from './nav/Nav';
import { Hello } from './screens/Hello';
import { MinionsList } from './screens/MinionsList';

export default function App() {
  const [screen, setScreen] = useState(SCREENS.HELLO);

  const screenRenderer = ((selectedScreen: SCREENS) => {
    switch (selectedScreen) {
      case SCREENS.HELLO:
        return <Hello />;
      case SCREENS.MINIONS_LIST:
        return <MinionsList episodes={[42]} />;
    }
  })(screen);

  return (
    <div>
      <Nav handleNav={setScreen} />
      {screenRenderer}
    </div>
  );
}
