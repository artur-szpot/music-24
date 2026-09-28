import { useEffect, useState } from 'react';
import { RuntimeConfig, RuntimeConfigKey } from '../../constants/runtimeConfig';

const PATHS: { key: RuntimeConfigKey; label: string }[] = [
  { key: 'databasePath', label: 'SQLite database' },
  { key: 'minionRoot', label: 'Minion image root' },
  { key: 'cardRoot', label: 'Card image root' },
  { key: 'fileSystemRoot', label: 'General file-system image root' },
];

export default function Settings({ onClose }: { onClose: () => void }) {
  const [paths, setPaths] = useState<RuntimeConfig>();
  const [busy, setBusy] = useState(false);
  const [restarting, setRestarting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let mounted = true;
    window.electron.config
      .get()
      .then((config) => {
        if (mounted) setPaths(config);
        return undefined;
      })
      .catch(() => {
        if (mounted) setError('Could not load the active configuration.');
      });
    return () => {
      mounted = false;
    };
  }, []);

  const choose = async (key: RuntimeConfigKey) => {
    setBusy(true);
    setError('');
    try {
      const selected = await window.electron.config.choose(key);
      if (selected)
        setPaths((current) => current && { ...current, [key]: selected });
    } catch {
      setError('Could not select a path.');
    } finally {
      setBusy(false);
    }
  };

  const apply = async () => {
    if (!paths) return;
    setBusy(true);
    setError('');
    try {
      const result = await window.electron.config.apply(paths);
      if (result.errors.length) {
        setError(result.errors.join(' '));
      } else if (result.restarting) {
        setRestarting(true);
      } else {
        onClose();
      }
    } catch {
      setError(
        'Could not save the configuration. Your current session is unchanged.',
      );
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="screen settings-screen">
      <h1>Collection settings</h1>
      <p>
        Review the active paths. Select replacements and restart to use them.
      </p>
      {error && <p role="alert">{error}</p>}
      {!paths && !error && <p>Loading paths…</p>}
      {paths && (
        <>
          {PATHS.map(({ key, label }) => (
            <div className="settings-row" key={key}>
              <label htmlFor={`settings-${key}`}>{label}</label>
              <input id={`settings-${key}`} value={paths[key]} readOnly />
              <button
                type="button"
                disabled={busy || restarting}
                onClick={() => choose(key)}
              >
                Choose…
              </button>
            </div>
          ))}
          <p>Changes are not saved until you select Save and restart.</p>
          <button type="button" disabled={busy || restarting} onClick={apply}>
            Save and restart
          </button>
        </>
      )}
      <button type="button" disabled={busy || restarting} onClick={onClose}>
        Cancel
      </button>
      {restarting && <p role="status">Restarting with the new paths…</p>}
    </main>
  );
}
