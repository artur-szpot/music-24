import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import EditIcon from '@mui/icons-material/Edit';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import { EpisodeChip } from './EpisodeChip';
import { FilterSubRow } from './FilterSubRow';

export interface ViewCategoryProps {
  oneOf?: number[];
  allOf?: number[];
  noneOf?: number[];
}

export interface FilterRowProps extends ViewCategoryProps {
  label: string;
  labels: Record<number, string>;
  noContents?: boolean;
  openSidePanel: () => void;
}

export const FilterRow: React.FC<FilterRowProps> = (props: FilterRowProps) => {
  const { label, allOf, oneOf, noneOf, labels, noContents, openSidePanel } =
    props;
  if (noContents) {
    return (
      <div className="filter-row">
        <h4>{label}</h4>
      </div>
    );
  }
  return (
    <div className="filter-row">
      <h4>{label}</h4>
      {oneOf && (
        <FilterSubRow
          ids={oneOf}
          label="Any of"
          labels={labels}
          openSidePanel={openSidePanel}
        />
      )}
      {(allOf || noneOf) && (
        <FilterSubRow
          ids={allOf}
          negativeIds={noneOf}
          label={allOf && noneOf ? 'All/none of' : allOf ? 'All of' : 'None of'}
          labels={labels}
          openSidePanel={openSidePanel}
        />
      )}
      <Stack direction="row" spacing={1}>
        {oneOf === undefined && (
          <Chip
            label="One of..."
            onClick={() => null}
            icon={<AddCircleIcon />}
          />
        )}
        {allOf === undefined && noneOf === undefined && (
          <Chip
            label="All/none of..."
            onClick={() => null}
            icon={<AddCircleIcon />}
          />
        )}
      </Stack>
    </div>
  );
};
