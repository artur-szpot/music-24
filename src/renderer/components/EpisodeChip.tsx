import Chip from '@mui/material/Chip';
import Tooltip from '@mui/material/Tooltip';
import React from 'react';
import { Minion } from './Minion';
import { SetScreenProps } from '../setScreenProps';
import { MinionDetails } from '../screens/MinionDetails';
import Typography from '@mui/material/Typography';

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
    color,
    onClick = () => null,
    onDelete = () => null,
  } = props;
  return (
    <Tooltip
      title={
        <React.Fragment>
          <Typography color="inherit">Tooltip with HTML</Typography>
          <em>{"And here's"}</em> <b>{'some'}</b> <u>{'amazing content'}</u>.{' '}
          {"It's very engaging. Right?"}
          <MinionDetails id={id} />
        </React.Fragment>
      }
      sx={{ maxWidth: '400px' }}
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
