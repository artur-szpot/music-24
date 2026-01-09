import Chip from '@mui/material/Chip';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import React from 'react';
import { SCREEN_TYPES } from '../../enums/screens';
import { MinionDetails } from '../screens/MinionDetails';

export interface CustomChipProps {
  id: number;
  label: string;
  color?:
    | 'default'
    | 'primary'
    | 'secondary'
    | 'error'
    | 'info'
    | 'success'
    | 'warning';
  onClick?: (id: number) => void;
  onDelete?: (id: number) => void;
}

export const EpisodeChip: React.FC<CustomChipProps> = (
  props: CustomChipProps,
) => {
  const {
    id,
    label,
    color = 'primary',
    onClick = () => null,
    onDelete = () => null,
  } = props;
  return (
    <Tooltip
      title={
        <React.Fragment>
          <MinionDetails id={id} screenType={SCREEN_TYPES.TOOLTIP} />
        </React.Fragment>
      }
      sx={{ maxWidth: '250px' }}
      followCursor={true}
    >
      <Chip
        label={label}
        color={color}
        onClick={() => onClick(id)}
        onDelete={() => onDelete(id)}
      />
    </Tooltip>
  );
};
