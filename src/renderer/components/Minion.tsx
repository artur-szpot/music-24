import { SCREENS } from '../../enums/screens';
import { Interactive } from './interactive';

export interface MinionOwnProps {
  id: number;
  url: string;
  episode: number;
  scene: number;
  caption?: string;
  fullSize?: boolean;
  onClick?: () => void;
}

export interface MinionProps extends Interactive, MinionOwnProps {}

const minionUrl = (episode: number, url: string) =>
  `minion:///${episode}/${url}`;

export const Minion: React.FC<MinionOwnProps> = (props: MinionOwnProps) => {
  const { id, url, episode, caption, fullSize, onClick = () => null } = props;
  return (
    <div className={`minion ${fullSize ? 'full' : ''}`} key={`minion-${id}`}>
      <img src={minionUrl(episode, url)} onClick={onClick} />
      {caption && <p>{caption}</p>}
    </div>
  );
};

export const MinionInteractive: React.FC<MinionProps> = (
  props: MinionProps,
) => {
  const { id, fullSize } = props;
  return (
    <Minion
      {...props}
      onClick={
        fullSize
          ? () => null
          : () =>
              props.handleNav.setPopup({
                screen: SCREENS.MINION_DETAILS,
                id,
              })
      }
    />
  );
};
