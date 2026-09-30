import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { CardSubRow, IpcResult, TAG_RELATION } from '../../constants/dbIpc';
import { LIMITS } from '../../constants/limits';
import { LoaderScreen } from '../components/Loader';
import { Interactive } from '../interfaces/interactive';
import { ScreenProps } from '../interfaces/screen';
import { navTo } from '../interfaces/setScreenProps';
import { TagDetailsOwnProps } from './TagDetailsProps';

export interface TagDetailsProps
  extends Interactive,
    TagDetailsOwnProps,
    ScreenProps {}

interface ActiveForm {
  kind: 'rename' | 'add';
  id: number;
}

const DELETE_CONFLICT =
  'Only tags without subs and without images can be removed.';

export const TagDetails: React.FC<TagDetailsProps> = (
  props: TagDetailsProps,
) => {
  const { id, handleNav } = props;
  const [rows, setRows] = useState<CardSubRow[]>([]);
  const [isDataLoading, setIsDataLoading] = useState(true);
  const [error, setError] = useState('');
  const [actionError, setActionError] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [activeForm, setActiveForm] = useState<ActiveForm | undefined>(
    undefined,
  );
  const [formValue, setFormValue] = useState('');
  const [reloadToken, setReloadToken] = useState(0);

  useEffect(() => {
    let active = true;
    setIsDataLoading(true);
    window.electron.database
      .cardSubs(id)
      .then((result) => {
        if (!active) return undefined;
        if (result.ok) {
          setRows(result.data);
          setError(result.data.length ? '' : 'Tag not found.');
        } else {
          setError(result.error.message);
        }
        setIsDataLoading(false);
        return undefined;
      })
      .catch(() => {
        if (active) {
          setError('Could not load tag.');
          setIsDataLoading(false);
        }
      });
    return () => {
      active = false;
    };
  }, [id, reloadToken]);

  const childrenByParent = useMemo(() => {
    const map = new Map<number, CardSubRow[]>();
    rows.forEach((row) => {
      if (row.parent === null) return;
      map.set(row.parent, [...(map.get(row.parent) ?? []), row]);
    });
    return map;
  }, [rows]);

  const subtreeIds = useCallback(
    (rootId: number): number[] => {
      const collected: number[] = [];
      const queue = [rootId];
      while (queue.length) {
        const current = queue.shift() as number;
        collected.push(current);
        (childrenByParent.get(current) ?? []).forEach((child) =>
          queue.push(child.id),
        );
      }
      return collected;
    },
    [childrenByParent],
  );

  const runAction = async (
    action: () => Promise<IpcResult<boolean>>,
    conflictMessage: string,
    onSuccess?: () => void,
  ) => {
    setActionError('');
    setIsSaving(true);
    try {
      const result = await action();
      if (!result.ok) {
        setActionError(result.error.message);
      } else if (!result.data) {
        setActionError(conflictMessage);
      } else {
        setActiveForm(undefined);
        setFormValue('');
        if (onSuccess) onSuccess();
        else setReloadToken((token) => token + 1);
      }
    } catch {
      setActionError('Could not update tags.');
    } finally {
      setIsSaving(false);
    }
  };

  if (isDataLoading) return <LoaderScreen />;

  const root = rows.find((row) => row.id === id);
  if (error || !root)
    return (
      <div className="screen" role="alert">
        {error || 'Tag not found.'}
      </div>
    );

  const openForm = (kind: 'rename' | 'add', target: CardSubRow) => {
    setActionError('');
    setActiveForm({ kind, id: target.id });
    setFormValue(kind === 'rename' ? target.name : '');
  };

  const renderForm = (target: CardSubRow) => {
    if (activeForm?.id !== target.id) return null;
    const isRename = activeForm.kind === 'rename';
    return (
      <Stack direction="row" spacing={1} className="tag-form">
        <TextField
          autoFocus
          size="small"
          label={isRename ? 'Tag name' : 'New sub name'}
          value={formValue}
          onChange={(event) => setFormValue(event.target.value)}
        />
        <Button
          disabled={isSaving || !formValue.trim()}
          onClick={() =>
            runAction(
              () =>
                isRename
                  ? window.electron.database.renameCard(target.id, formValue)
                  : window.electron.database.createCard(target.id, formValue),
              isRename
                ? 'Tag no longer exists.'
                : 'Parent tag no longer exists.',
            )
          }
        >
          {isRename ? 'Save name' : 'Create sub'}
        </Button>
        <Button
          disabled={isSaving}
          onClick={() => {
            setActiveForm(undefined);
            setFormValue('');
          }}
        >
          Cancel
        </Button>
      </Stack>
    );
  };

  const renderCounts = (target: CardSubRow) => {
    const ids = subtreeIds(target.id);
    const hasSubs = ids.length > 1;
    return (
      <Stack direction="row" spacing={1} className="tag-counts">
        <Button
          disabled={!target.total}
          onClick={() =>
            handleNav.setScreen(
              navTo.minionList({
                query: { cards: [target.id], rel: TAG_RELATION },
              }),
            )
          }
        >
          {`${target.total} images directly`}
        </Button>
        {hasSubs && (
          <Button
            disabled={!target.subtreeTotal || ids.length > LIMITS.MAX_QUERY_IDS}
            onClick={() =>
              handleNav.setScreen(
                navTo.minionList({ query: { cards: ids, rel: TAG_RELATION } }),
              )
            }
          >
            {`${target.subtreeTotal} images including ${ids.length - 1} subs`}
          </Button>
        )}
      </Stack>
    );
  };

  const renderActions = (target: CardSubRow, isRoot: boolean) => (
    <Stack direction="row" spacing={1} className="tag-actions">
      <Button disabled={isSaving} onClick={() => openForm('rename', target)}>
        Rename
      </Button>
      <Button disabled={isSaving} onClick={() => openForm('add', target)}>
        Add sub
      </Button>
      <Button
        color="error"
        disabled={isSaving}
        onClick={() =>
          runAction(
            () => window.electron.database.deleteCard(target.id),
            DELETE_CONFLICT,
            isRoot
              ? () =>
                  handleNav.setScreen(
                    target.parent === null
                      ? navTo.tagsList({})
                      : navTo.tagDetails({ id: target.parent }),
                  )
              : undefined,
          )
        }
      >
        Remove
      </Button>
    </Stack>
  );

  const subs = childrenByParent.get(root.id) ?? [];

  return (
    <div className="screen card-details-screen">
      <div className="card-screen-contents">
        <h1>{root.name}</h1>
        <p>{`Category: ${root.category ?? 'None'}`}</p>
        {root.parent !== null && (
          <Button
            onClick={() =>
              handleNav.setScreen(
                navTo.tagDetails({ id: root.parent as number }),
              )
            }
          >
            Up to parent tag
          </Button>
        )}
        {renderCounts(root)}
        {renderActions(root, true)}
        {renderForm(root)}
        {actionError && <p role="alert">{actionError}</p>}
        <section className="tag-subs">
          <h2>{`Subs (${subs.length})`}</h2>
          {!subs.length && <p>This tag has no subs.</p>}
          <ul className="tag-sub-list">
            {subs.map((sub) => (
              <li key={sub.id}>
                <Button
                  className="tag-sub-name"
                  onClick={() =>
                    handleNav.setScreen(navTo.tagDetails({ id: sub.id }))
                  }
                >
                  {`${sub.name}${
                    (childrenByParent.get(sub.id) ?? []).length
                      ? ` (${(childrenByParent.get(sub.id) ?? []).length} subs)`
                      : ''
                  }`}
                </Button>
                {renderCounts(sub)}
                {renderActions(sub, false)}
                {renderForm(sub)}
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
};
