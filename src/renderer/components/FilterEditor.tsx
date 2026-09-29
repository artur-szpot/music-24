import AddIcon from '@mui/icons-material/Add';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import Autocomplete from '@mui/material/Autocomplete';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuItem from '@mui/material/MenuItem';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import React from 'react';
import { FilterCategory, MinionFilter } from '../../constants/dbIpc';
import { GlobalLabels } from '../globalLabels';

type FilterDimension = 'cards' | 'seasons' | 'episodes' | 'scenes';
type FilterOperator = keyof FilterCategory;

interface FilterEditorProps {
  filter: MinionFilter;
  globalLabels: GlobalLabels;
  onChange: (filter: MinionFilter) => void;
  onRemove: (() => void) | undefined;
}

interface CategoryEditorProps {
  title: string;
  category: FilterCategory | undefined;
  labels: Record<number, string>;
  onChange: (category: FilterCategory) => void;
}

const operatorLabels: Record<FilterOperator, string> = {
  oneOf: 'Any of',
  allOf: 'All of',
  noneOf: 'None of',
};

function CategoryEditor({
  title,
  category = {},
  labels,
  onChange,
}: CategoryEditorProps): React.ReactElement {
  const update = (operator: FilterOperator, ids: number[]) => {
    const next = { ...category };
    if (ids.length) next[operator] = ids;
    else delete next[operator];
    onChange(next);
  };
  const options = Array.from(
    new Set([
      ...Object.keys(labels).map(Number),
      ...Object.values(category).flat(),
    ]),
  );

  return (
    <fieldset className="filter-editor-category">
      <legend>{title}</legend>
      <Stack spacing={1}>
        {(Object.keys(operatorLabels) as FilterOperator[]).map((operator) => (
          <Autocomplete<number, true, false, false>
            key={operator}
            multiple
            options={options}
            value={category[operator] ?? []}
            getOptionLabel={(id) => labels[id] ?? `#${id}`}
            isOptionEqualToValue={(option, value) => option === value}
            onChange={(_event, ids) => update(operator, ids)}
            renderInput={(params) => (
              <TextField
                // eslint-disable-next-line react/jsx-props-no-spreading
                {...params}
                label={`${operatorLabels[operator]} ${title.toLowerCase()}`}
                size="small"
              />
            )}
          />
        ))}
      </Stack>
    </fieldset>
  );
}

function replaceCategory(
  filter: MinionFilter,
  dimension: FilterDimension,
  category: FilterCategory,
): MinionFilter {
  const next = { ...filter };
  if (dimension === 'cards') next.cards = category;
  if (dimension === 'seasons') next.seasons = category;
  if (dimension === 'episodes') next.episodes = category;
  if (dimension === 'scenes') next.scenes = category;
  return next;
}

export default function FilterEditor({
  filter,
  globalLabels,
  onChange,
  onRemove,
}: FilterEditorProps): React.ReactElement {
  const changeNested = (index: number, child: MinionFilter) => {
    const views = [...(filter.views ?? [])];
    views[index] = child;
    onChange({ ...filter, views });
  };
  const removeNested = (index: number) => {
    const views = (filter.views ?? []).filter(
      (_, childIndex) => childIndex !== index,
    );
    onChange({ ...filter, views: views.length ? views : undefined });
  };

  return (
    <fieldset className="filter-editor">
      <legend>Filter conditions</legend>
      <Stack spacing={2}>
        <Stack direction="row" spacing={1} alignItems="center">
          <TextField
            select
            label="Match"
            size="small"
            value={filter.logic}
            onChange={(event) =>
              onChange({
                ...filter,
                logic: event.target.value as MinionFilter['logic'],
              })
            }
          >
            <MenuItem value="all">All conditions</MenuItem>
            <MenuItem value="any">Any condition</MenuItem>
          </TextField>
          {onRemove && (
            <IconButton
              aria-label="Remove nested filter"
              onClick={onRemove}
              size="small"
            >
              <DeleteOutlineIcon />
            </IconButton>
          )}
        </Stack>
        <CategoryEditor
          title="Cards and tags"
          category={filter.cards}
          labels={globalLabels.cards}
          onChange={(category) =>
            onChange(replaceCategory(filter, 'cards', category))
          }
        />
        <CategoryEditor
          title="Seasons"
          category={filter.seasons}
          labels={globalLabels.seasons}
          onChange={(category) =>
            onChange(replaceCategory(filter, 'seasons', category))
          }
        />
        <CategoryEditor
          title="Episodes"
          category={filter.episodes}
          labels={globalLabels.episodes}
          onChange={(category) =>
            onChange(replaceCategory(filter, 'episodes', category))
          }
        />
        <CategoryEditor
          title="Scenes"
          category={filter.scenes}
          labels={globalLabels.scenes}
          onChange={(category) =>
            onChange(replaceCategory(filter, 'scenes', category))
          }
        />
        {(filter.views ?? []).map((child, index) => (
          <FilterEditor
            // eslint-disable-next-line react/no-array-index-key
            key={`nested-filter-${index}`}
            filter={child}
            globalLabels={globalLabels}
            onChange={(next) => changeNested(index, next)}
            onRemove={() => removeNested(index)}
          />
        ))}
        <Button
          startIcon={<AddIcon />}
          onClick={() =>
            onChange({
              ...filter,
              views: [...(filter.views ?? []), { logic: 'all' }],
            })
          }
        >
          Add nested filter
        </Button>
      </Stack>
    </fieldset>
  );
}
