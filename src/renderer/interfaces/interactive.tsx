import { GlobalLabels } from '../globalLabels';
import { SetScreenProps } from './setScreenProps';

export interface Interactive {
  handleNav: {
    setScreen: (props: SetScreenProps) => void;
    setPopup: (props: SetScreenProps) => void;
  };
  globalLabels: GlobalLabels;
}
