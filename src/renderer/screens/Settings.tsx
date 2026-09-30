import { useEffect, useState } from 'react';
import FolderOpenOutlinedIcon from '@mui/icons-material/FolderOpenOutlined';
import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import IconButton from '@mui/material/IconButton';
import InputAdornment from '@mui/material/InputAdornment';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { RuntimeConfig, RuntimeConfigKey } from '../../constants/runtimeConfig';

const PATHS: { key: RuntimeConfigKey; label: string }[] = [
  { key: 'databasePath', label: 'SQLite database' },
  { key: 'minionRoot', label: 'Minion image root' },
  { key: 'cardRoot', label: 'Card image root' },
  { key: 'fileSystemRoot', label: 'General file-system image root' },
  { key: 'outputDirectory', label: 'Minion copy output directory' },
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
      .then((result) => {
        if (mounted) {
          if (result.ok) setPaths(result.data);
          else setError(result.error.message);
        }
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
      const result = await window.electron.config.choose(key);
      if (!result.ok) setError(result.error.message);
      else if (result.data)
        setPaths((current) => current && { ...current, [key]: result.data });
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
      if (!result.ok) {
        setError(result.error.message);
      } else if (result.data.restarting) {
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
      <Box className="settings-content">
        <Typography variant="h1" gutterBottom>
          Collection settings
        </Typography>
        <Typography color="text.secondary" paragraph>
          Review the active paths. Select replacements and restart to use them.
        </Typography>
        {error && (
          <Alert severity="error" role="alert" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        {!paths && !error && (
          <Stack direction="row" spacing={1} alignItems="center">
            <CircularProgress size={18} />
            <Typography>Loading paths...</Typography>
          </Stack>
        )}
        {paths && (
          <>
            <Stack spacing={2} className="settings-paths">
              {PATHS.map(({ key, label }) => (
                <TextField
                  key={key}
                  id={`settings-${key}`}
                  label={label}
                  value={paths[key] ?? ''}
                  fullWidth
                  size="small"
                  InputProps={{
                    readOnly: true,
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label={`Choose ${label}`}
                          edge="end"
                          disabled={busy || restarting}
                          onClick={() => choose(key)}
                        >
                          <FolderOpenOutlinedIcon />
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              ))}
            </Stack>
            {!paths.outputDirectory && (
              <Alert severity="info" role="note" sx={{ mt: 2 }}>
                Choose an output directory to enable copying minions.
              </Alert>
            )}
            <Typography color="text.secondary" sx={{ mt: 2 }}>
              Changes are not saved until you select Save and restart.
            </Typography>
            <Stack direction="row" spacing={1} sx={{ mt: 3 }}>
              <Button
                variant="contained"
                disabled={busy || restarting}
                onClick={apply}
              >
                {busy ? 'Saving...' : 'Save and restart'}
              </Button>
              <Button disabled={busy || restarting} onClick={onClose}>
                Cancel
              </Button>
            </Stack>
          </>
        )}
        {restarting && (
          <Alert severity="info" role="status" sx={{ mt: 2 }}>
            Restarting with the new paths...
          </Alert>
        )}
      </Box>
    </main>
  );
}
