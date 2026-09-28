import { navTo, SetScreenProps } from '../interfaces/setScreenProps';

export function Nav(props: {
  handleNav: (props: SetScreenProps) => void;
  onSettings: () => void;
}) {
  const { handleNav, onSettings } = props;
  return (
    <div id="nav">
      <button onClick={() => handleNav(navTo.minionDetails({ id: 1003 }))}>
        Minion details
      </button>
      <button onClick={() => handleNav(navTo.cardDetails({ id: 1038 }))}>
        Card details
      </button>
      <button onClick={() => handleNav(navTo.minionList({ query: {} }))}>
        Minion list
      </button>
      <button onClick={() => handleNav(navTo.tagsList({}))}>Tags</button>
      <button onClick={() => handleNav(navTo.scenesList({}))}>Scenes</button>
      <button onClick={() => handleNav(navTo.cardImplementationsList({}))}>
        Card implementations
      </button>
      <button type="button" onClick={onSettings}>
        Settings
      </button>
    </div>
  );
}
