import { SCREENS } from '../../enums/screens';
import { Interactive } from './interactive';

export enum MINION_SIZES {
  LIST = 'minion-list',
  SOLO = 'minion-solo',
  FULL = 'minion-full',
}

export interface MinionOwnProps {
  id: number;
  url: string;
  episode: number;
  scene: number;
  caption?: string;
  size?: MINION_SIZES;
  onClick?: () => void;
}

export interface MinionProps extends MinionOwnProps {
  onClick: () => void;
}

const minionUrl = (episode: number, url: string) =>
  `minion:///${episode}/${url}`;

export const Minion: React.FC<MinionOwnProps> = (props: MinionOwnProps) => {
  const {
    id,
    url,
    episode,
    caption,
    size = MINION_SIZES.LIST,
    onClick = () => null,
  } = props;
  return (
    <div className={`minion ${size}`} key={`minion-${id}`}>
      <img src={minionUrl(episode, url)} onClick={onClick} />
      {caption && <p>{caption}</p>}
    </div>
  );
};

export const MinionInteractive: React.FC<MinionProps> = (
  props: MinionProps,
) => {
  const { onClick } = props;
  return <Minion {...props} onClick={() => onClick} />;
};
