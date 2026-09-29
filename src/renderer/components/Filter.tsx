import { GlobalLabels } from '../globalLabels';
import { MinionFilter } from '../../constants/dbIpc';
import { FilterRow } from './FilterRow';

export interface FilterProps extends MinionFilter {
  globalLabels: GlobalLabels;
  openSidePanel: () => void;
}

export const Filter: React.FC<FilterProps> = (props: FilterProps) => {
  const {
    logic,
    cards,
    episodes,
    scenes,
    seasons,
    views,
    globalLabels,
    openSidePanel,
  } = props;

  return (
    <div className="filter-main">
      <h3>
        {logic === 'all'
          ? 'All of the following conditions:'
          : 'Any of the following conditions:'}
      </h3>
      {cards && (
        <FilterRow
          label="Cards & tags"
          {...cards}
          labels={globalLabels.cards}
          openSidePanel={openSidePanel}
        />
      )}
      {seasons && (
        <FilterRow
          label="Seasons"
          {...seasons}
          labels={globalLabels.seasons}
          openSidePanel={openSidePanel}
        />
      )}
      {episodes && (
        <FilterRow
          label="Episodes"
          {...episodes}
          labels={globalLabels.episodes}
          openSidePanel={openSidePanel}
        />
      )}
      {scenes && (
        <FilterRow
          label="Scenes"
          {...scenes}
          labels={globalLabels.scenes}
          openSidePanel={openSidePanel}
        />
      )}
      {views && (
        <FilterRow
          label="Complex filters"
          noContents={true}
          labels={globalLabels.scenes}
          openSidePanel={openSidePanel}
        />
      )}
      {(views ?? []).map((view) => (
        <Filter
          {...view}
          globalLabels={globalLabels}
          openSidePanel={openSidePanel}
        />
      ))}
    </div>
  );
};
