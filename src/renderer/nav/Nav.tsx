import { SCREENS } from '../../enums/screens';

export function Nav(props: { handleNav: (screen: SCREENS) => void }) {
  const { handleNav } = props;
  return (
    <div id="nav">
      <button onClick={() => handleNav(SCREENS.HELLO)}>Test screen</button>
      <button onClick={() => handleNav(SCREENS.MINION_DETAILS)}>
        Minion details
      </button>
      <button onClick={() => handleNav(SCREENS.MINIONS_LIST)}>
        Minion list
      </button>
    </div>
  );
}
