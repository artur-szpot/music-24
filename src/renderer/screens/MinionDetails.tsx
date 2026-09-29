import React, { useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import Chip from '@mui/material/Chip';
import { MinionSource } from '../../constants/dbIpc';
import { LoaderScreen } from '../components/Loader';
import { Minion, MINION_SIZES, MinionOwnProps } from '../components/Minion';
import { SCREEN_TYPES } from '../../enums/screens';
import { MinionDetailsOwnProps } from './MinionDetailsProps';
import { ScreenProps } from '../interfaces/screen';
import { Interactive } from '../interfaces/interactive';
import { navTo } from '../interfaces/setScreenProps';
import { MinionCardRow, MinionQuery } from '../../constants/dbIpc';

interface CardTreeNode extends MinionCardRow {
  children: CardTreeNode[];
}

function buildCardTree(cards: MinionCardRow[]): CardTreeNode[] {
  const nodes = new Map<number, CardTreeNode>();
  cards.forEach((card) => nodes.set(card.id, { ...card, children: [] }));
  const roots: CardTreeNode[] = [];
  nodes.forEach((node) => {
    const parent = node.parent === null ? undefined : nodes.get(node.parent);
    if (parent) parent.children.push(node);
    else roots.push(node);
  });
  return roots;
}

export interface MinionDetailsProps
  extends MinionDetailsOwnProps,
    Partial<Interactive>,
    ScreenProps {}

export const MinionDetails: React.FC<MinionDetailsProps> = (
  props: MinionDetailsProps,
) => {
  const { id, screenType, handleNav, globalLabels } = props;
  const [minion, setMinion] = useState<MinionOwnProps | undefined>(undefined);
  const [relatedCards, setRelatedCards] = useState<MinionCardRow[]>([]);
  const [areRelatedCardsLoading, setAreRelatedCardsLoading] = useState(true);
  const [relatedCardsError, setRelatedCardsError] = useState('');
  const [source, setSource] = useState<MinionSource | undefined>(undefined);
  const [sourceError, setSourceError] = useState('');
  const [copyMessage, setCopyMessage] = useState('');
  const [copyError, setCopyError] = useState('');
  const [isCopying, setIsCopying] = useState(false);
  const [outputConfigured, setOutputConfigured] = useState(false);
  const [isDataLoading, setIsDataLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    setIsDataLoading(true);
    window.electron.database
      .minions({ ids: [id] }, 0)
      .then((result) => {
        if (!active) return undefined;
        if (result.ok) {
          setMinion(result.data[0]);
          setError(result.data.length ? '' : 'Image not found.');
        } else {
          setError(result.error.message);
        }
        setIsDataLoading(false);
        return undefined;
      })
      .catch(() => {
        if (active) {
          setError('Could not load image.');
          setIsDataLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [id]);

  useEffect(() => {
    let active = true;
    window.electron.database
      .minionSource(id)
      .then((result) => {
        if (!active) return;
        if (result.ok) setSource(result.data);
        else setSourceError(result.error.message);
      })
      .catch(() => {
        if (active) setSourceError('Could not load source file details.');
      });
    window.electron.config
      .get()
      .then((result) => {
        if (active && result.ok)
          setOutputConfigured(Boolean(result.data.outputDirectory));
      })
      .catch(() => undefined);
    return () => {
      active = false;
    };
  }, [id]);

  const revealSource = async () => {
    setCopyError('');
    setCopyMessage('');
    try {
      const result = await window.electron.database.revealMinion(id);
      if (!result.ok) setCopyError(result.error.message);
    } catch {
      setCopyError('Could not reveal the source file.');
    }
  };

  const copyToOutput = async () => {
    setIsCopying(true);
    setCopyError('');
    setCopyMessage('');
    try {
      const result = await window.electron.database.copyMinion(id);
      if (result.ok) setCopyMessage('Copied to output directory.');
      else setCopyError(result.error.message);
    } catch {
      setCopyError('Could not copy the minion file.');
    } finally {
      setIsCopying(false);
    }
  };

  useEffect(() => {
    let active = true;
    setAreRelatedCardsLoading(true);
    setRelatedCardsError('');
    window.electron.database
      .minionCards(id)
      .then((result) => {
        if (!active) return;
        if (result.ok) {
          setRelatedCards(result.data);
        } else {
          setRelatedCardsError(result.error.message);
        }
        setAreRelatedCardsLoading(false);
      })
      .catch(() => {
        if (active) {
          setRelatedCardsError('Could not load related cards.');
          setAreRelatedCardsLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [id]);

  if (isDataLoading) {
    return <LoaderScreen />;
  }
  if (error || !minion)
    return (
      <div className={screenType} role="alert">
        {error || 'Image not found.'}
      </div>
    );

  const size = ((_screenType: SCREEN_TYPES) => {
    switch (_screenType) {
      case SCREEN_TYPES.SCREEN:
      case SCREEN_TYPES.POPUP:
        return MINION_SIZES.SOLO;
      case SCREEN_TYPES.SIDE_PANEL:
      case SCREEN_TYPES.TOOLTIP:
        return MINION_SIZES.FULL;
      default:
        throw new Error(`Screen type not covered: ${_screenType}`);
    }
  })(screenType);

  const metadataChip = (
    category: string,
    label: React.ReactNode,
    query: MinionQuery,
  ) => {
    return (
      <Chip
        label={`${category}: ${label}`}
        size="small"
        onClick={
          handleNav
            ? () => handleNav.setScreen(navTo.minionList({ query }))
            : undefined
        }
        style={{ flex: '0 0 auto' }}
      ></Chip>
    );
  };

  const metadata = (
    <div
      className="minion-metadata"
      role="group"
      aria-label="Minion metadata"
      style={{
        display: 'flex',
        flexWrap: 'nowrap',
        gap: 8,
        maxWidth: '100%',
        overflowX: 'auto',
      }}
    >
      {minion.season !== undefined &&
        minion.season !== null &&
        metadataChip(
          'Season',
          globalLabels?.seasons[minion.season] ?? `Season ${minion.season}`,
          { seasons: [minion.season] },
        )}
      {metadataChip(
        'Episode',
        globalLabels?.episodes[minion.episode] ?? minion.episode,
        { episodes: [minion.episode] },
      )}
      {metadataChip(
        'Scene',
        globalLabels?.scenes[minion.scene] ?? minion.scene,
        { scenes: [minion.scene] },
      )}
    </div>
  );
  const cardTree = buildCardTree(relatedCards);
  const renderCardNodes = (nodes: CardTreeNode[]): React.ReactNode => (
    <ul>
      {nodes.map((node) => (
        <li key={node.id}>
          {node.name} {node.isSelected ? '(selected)' : '(parent)'}
          {node.children.length > 0 && renderCardNodes(node.children)}
        </li>
      ))}
    </ul>
  );
  const relatedCardsContent = (
    <section className="minion-related-cards">
      <h2>Related cards</h2>
      {areRelatedCardsLoading ? (
        <p role="status">Loading related cards...</p>
      ) : relatedCardsError ? (
        <p role="alert">{relatedCardsError}</p>
      ) : relatedCards.length ? (
        <>
          <p>{`${relatedCards.filter((card) => card.isSelected).length} cards selected`}</p>
          {renderCardNodes(cardTree)}
        </>
      ) : (
        <p>No cards selected.</p>
      )}
    </section>
  );
  const fileActions = (
    <section className="minion-file-actions">
      <h2>Source file</h2>
      {sourceError ? (
        <p role="alert">{sourceError}</p>
      ) : source ? (
        <>
          <p>{source.fileName}</p>
          <p>{source.fullPath}</p>
          <Button onClick={revealSource}>Show in Explorer</Button>
          <Button
            disabled={!outputConfigured || isCopying}
            onClick={copyToOutput}
          >
            {isCopying ? 'Copying...' : 'Copy to output'}
          </Button>
          {!outputConfigured && (
            <p>Choose an output directory in Settings to enable copying.</p>
          )}
          {copyMessage && <p role="status">{copyMessage}</p>}
          {copyError && <p role="alert">{copyError}</p>}
        </>
      ) : (
        <p role="status">Loading source file...</p>
      )}
    </section>
  );

  switch (size) {
    case MINION_SIZES.SOLO:
      return (
        <div className={screenType}>
          <div className="minion-screen-contents">
            <Minion {...minion} size={size} />
            {metadata}
            {relatedCardsContent}
            {fileActions}
          </div>
        </div>
      );
    default:
      return (
        <div className={screenType}>
          <Minion {...minion} size={size} />
          {metadata}
          {relatedCardsContent}
          {fileActions}
        </div>
      );
  }
};
