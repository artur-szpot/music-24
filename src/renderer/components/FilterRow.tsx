import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import EditIcon from '@mui/icons-material/Edit';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import { EpisodeChip } from './EpisodeChip';

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

interface FilterSubRowProps {
  ids?: number[];
  negativeIds?: number[];
  label: string;
  labels: Record<number, string>;
  openSidePanel: () => void;
}

const FilterSubRow: React.FC<FilterSubRowProps> = (
  props: FilterSubRowProps,
) => {
  const { ids, negativeIds, label, labels, openSidePanel } = props;
  return (
    <div className="filter-subrow">
      <Stack direction="row" spacing={1} useFlexGap sx={{ flexWrap: 'wrap' }}>
        <Chip label={label} onClick={() => openSidePanel} icon={<EditIcon />} />
        {(ids ?? []).map((id) => (
          <EpisodeChip id={id} label={labels[id]} />
        ))}
        {(negativeIds ?? []).map((id) => (
          <EpisodeChip id={id} label={labels[id]} color="error" />
        ))}
      </Stack>
    </div>
  );
};

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
