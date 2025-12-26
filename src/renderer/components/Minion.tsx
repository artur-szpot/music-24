import path from 'path';

export interface MinionProps {
  id: number;
  url: string;
  episode: number;
  scene: number;
}

const minionUrl = (episode: number, url: string) =>
  `minion:///${episode}/${url}`;

export const Minion: React.FC<MinionProps> = (props: MinionProps) => {
  const { id, url, episode } = props;
  return (
    <div className="minion" key={`minion-${id}`}>
      <img height="400px" src={minionUrl(episode, url)} />
    </div>
  );
};
