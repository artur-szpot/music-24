import EditIcon from '@mui/icons-material/Edit';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import { EpisodeChip } from './EpisodeChip';

interface FilterSubRowProps {
  ids?: number[];
  negativeIds?: number[];
  label: string;
  labels: Record<number, string>;
  openSidePanel: (newOpen: boolean) => void;
}

export const FilterSubRow: React.FC<FilterSubRowProps> = (
  props: FilterSubRowProps,
) => {
  const { ids, negativeIds, label, labels, openSidePanel } = props;
  return (
    <div className="filter-subrow">
      <Stack direction="row" spacing={1} useFlexGap sx={{ flexWrap: 'wrap' }}>
        <Chip
          label={label}
          onClick={() => openSidePanel(true)}
          icon={<EditIcon />}
        />
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
