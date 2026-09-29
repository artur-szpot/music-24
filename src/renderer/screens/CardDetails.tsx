import React, { useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { Filter } from '../components/Filter';
import FilterEditor from '../components/FilterEditor';
import { LoaderScreen } from '../components/Loader';
import { Minion, MINION_SIZES } from '../components/Minion';
import { Interactive } from '../interfaces/interactive';
import Drawer from '@mui/material/Drawer';
import { MinionDetails } from './MinionDetails';
import { SCREEN_TYPES } from '../../enums/screens';
import { CardProps } from '../interfaces/card';
import { CardDetailsOwnProps } from './CardDetailsProps';
import { ScreenProps } from '../interfaces/screen';
import { MinionFilter, MinionRow } from '../../constants/dbIpc';
import { navTo } from '../interfaces/setScreenProps';

export interface CardDetailsProps
  extends Interactive,
    CardDetailsOwnProps,
    ScreenProps {}

export const CardDetails: React.FC<CardDetailsProps> = (
  props: CardDetailsProps,
) => {
  const { id, globalLabels, handleNav } = props;
  const [card, setCard] = useState<CardProps | undefined>(undefined);
  const [filter, setFilter] = useState<MinionFilter | undefined>(undefined);
  const [draftFilter, setDraftFilter] = useState<MinionFilter>({
    logic: 'all',
  });
  const [matchCount, setMatchCount] = useState<number | undefined>(undefined);
  const [representative, setRepresentative] = useState<MinionRow | undefined>(
    undefined,
  );
  const [isDataLoading, setIsDataLoading] = useState(true);
  const [isFilterLoading, setIsFilterLoading] = useState(false);
  const [error, setError] = useState('');
  const [filterError, setFilterError] = useState('');
  const [saveError, setSaveError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [representativeError, setRepresentativeError] = useState('');

  const [sidePanelContent, setSidePanelContent] = React.useState(
    <MinionDetails
      id={666}
      screenType={SCREEN_TYPES.SIDE_PANEL}
      globalLabels={globalLabels}
      handleNav={handleNav}
    />,
  );
  const [sidePanelOpen, setSidePanelOpen] = React.useState(false);

  const toggleSidePanel = (newOpen: boolean) => {
    setSidePanelOpen(newOpen);
  };

  useEffect(() => {
    let active = true;
    setIsDataLoading(true);
    window.electron.database
      .cards([id])
      .then((result) => {
        if (!active) return undefined;
        if (result.ok) {
          const loadedCard = result.data[0];
          setCard(loadedCard);
          setError(loadedCard ? '' : 'Card not found.');
          try {
            const loadedFilter = loadedCard?.view
              ? (JSON.parse(loadedCard.view) as MinionFilter)
              : undefined;
            setFilter(loadedFilter);
            setDraftFilter(loadedFilter ?? { logic: 'all' });
          } catch {
            setFilter(undefined);
            setDraftFilter({ logic: 'all' });
            setError('Card filter is not valid JSON.');
          }
        } else {
          setError(result.error.message);
        }
        setIsDataLoading(false);
        return undefined;
      })
      .catch(() => {
        if (active) {
          setError('Could not load card.');
          setIsDataLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [id]);

  const saveFilter = async () => {
    setIsSaving(true);
    setSaveError('');
    try {
      const result = await window.electron.database.updateCardFilter(
        id,
        draftFilter,
      );
      if (!result.ok) {
        setSaveError(result.error.message);
      } else if (!result.data) {
        setSaveError('Card no longer exists.');
      } else {
        setFilter(draftFilter);
        setIsEditing(false);
      }
    } catch {
      setSaveError('Could not save card filter.');
    } finally {
      setIsSaving(false);
    }
  };

  useEffect(() => {
    if (!filter) {
      setIsFilterLoading(false);
      setMatchCount(undefined);
      setFilterError('');
      return undefined;
    }

    let active = true;
    setIsFilterLoading(true);
    setFilterError('');
    window.electron.database
      .minionCount({ filter })
      .then((result) => {
        if (!active) return;
        if (result.ok) {
          setMatchCount(result.data);
        } else {
          setFilterError(result.error.message);
        }
        setIsFilterLoading(false);
      })
      .catch(() => {
        if (active) {
          setFilterError('Could not count matching images.');
          setIsFilterLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, [filter]);

  useEffect(() => {
    let active = true;
    setRepresentative(undefined);
    setRepresentativeError('');
    window.electron.database
      .minions({ cards: [id], random: true }, 0)
      .then((result) => {
        if (!active) return;
        if (result.ok) {
          setRepresentative(result.data[0]);
        } else {
          setRepresentativeError(result.error.message);
        }
      })
      .catch(() => {
        if (active) setRepresentativeError('Could not load representative.');
      });
    return () => {
      active = false;
    };
  }, [id]);

  if (isDataLoading) {
    return <LoaderScreen />;
  }
  if (error || !card)
    return (
      <div className="screen" role="alert">
        {error || 'Card not found.'}
      </div>
    );

  const { name, category } = card;

  return (
    <div className="screen card-details-screen">
      <div className="card-screen-contents">
        <h1>{name} </h1>
        <p>{`Category: ${category}`}</p>
        {filter && (
          <section className="card-filter-results">
            <h2>Matching minions</h2>
            {isFilterLoading ? (
              <p role="status">Counting matching minions...</p>
            ) : filterError ? (
              <p role="alert">{filterError}</p>
            ) : (
              <>
                <p>{`${matchCount ?? 0} minions match this filter.`}</p>
                <Button
                  disabled={!matchCount}
                  onClick={() =>
                    handleNav.setScreen(navTo.minionList({ query: { filter } }))
                  }
                >
                  View filtered minions
                </Button>
              </>
            )}
          </section>
        )}
        <section className="card-representative">
          <h2>Representative</h2>
          {representativeError ? (
            <p role="alert">{representativeError}</p>
          ) : representative ? (
            <Minion
              {...representative}
              size={MINION_SIZES.LIST}
              onClick={() =>
                handleNav.setPopup(
                  navTo.minionDetails({ id: representative.id }),
                )
              }
            />
          ) : (
            <p>No related minions.</p>
          )}
        </section>
        {isEditing ? (
          <>
            <FilterEditor
              filter={draftFilter}
              globalLabels={globalLabels}
              onChange={setDraftFilter}
              onRemove={undefined}
            />
            <Stack direction="row" spacing={1}>
              <Button disabled={isSaving} onClick={saveFilter}>
                {isSaving ? 'Saving...' : 'Save filter'}
              </Button>
              <Button
                disabled={isSaving}
                onClick={() => {
                  setDraftFilter(filter ?? { logic: 'all' });
                  setSaveError('');
                  setIsEditing(false);
                }}
              >
                Cancel
              </Button>
            </Stack>
            {saveError && <p role="alert">{saveError}</p>}
          </>
        ) : (
          <>
            {filter && (
              <Filter
                {...filter}
                globalLabels={globalLabels}
                openSidePanel={() => toggleSidePanel(true)}
              />
            )}
            <Button
              onClick={() => {
                setDraftFilter(filter ?? { logic: 'all' });
                setSaveError('');
                setIsEditing(true);
              }}
            >
              {filter ? 'Edit filter' : 'Add filter'}
            </Button>
          </>
        )}
      </div>
      <Drawer
        open={sidePanelOpen}
        anchor="right"
        onClose={() => toggleSidePanel(false)}
      >
        {sidePanelContent}
      </Drawer>
    </div>
  );
};
