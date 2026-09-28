import '@testing-library/jest-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { RuntimeConfig } from '../constants/runtimeConfig';
import Settings from '../renderer/screens/Settings';

const paths: RuntimeConfig = {
  databasePath: 'C:\\data\\collection.db',
  minionRoot: 'C:\\images\\minions',
  cardRoot: 'C:\\images\\cards',
  fileSystemRoot: 'C:\\images\\files',
};

describe('Settings', () => {
  const get = jest.fn();
  const choose = jest.fn();
  const apply = jest.fn();
  const onClose = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    get.mockResolvedValue({ ok: true, data: paths });
    window.electron = {
      config: { get, choose, apply },
      database: {
        labels: jest.fn(),
        categories: jest.fn(),
        cards: jest.fn(),
        minions: jest.fn(),
        minionCount: jest.fn(),
      },
    };
  });

  it('shows active paths and discards an unsaved selection on cancel', async () => {
    choose.mockResolvedValue({ ok: true, data: 'C:\\other\\minions' });
    render(<Settings onClose={onClose} />);
    expect(
      await screen.findByDisplayValue(paths.minionRoot),
    ).toBeInTheDocument();
    fireEvent.click(
      screen
        .getByLabelText('Minion image root')
        .parentElement!.querySelector('button')!,
    );
    expect(
      await screen.findByDisplayValue('C:\\other\\minions'),
    ).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Cancel' }));
    expect(onClose).toHaveBeenCalledTimes(1);
    expect(apply).not.toHaveBeenCalled();
  });

  it('retains the draft when validation fails and retries the full configuration', async () => {
    choose.mockResolvedValue({ ok: true, data: 'C:\\other\\minions' });
    apply.mockResolvedValueOnce({
      ok: false,
      error: { code: 'INVALID_REQUEST', message: 'Invalid image root.' },
    });
    render(<Settings onClose={onClose} />);
    await screen.findByDisplayValue(paths.minionRoot);
    fireEvent.click(
      screen
        .getByLabelText('Minion image root')
        .parentElement!.querySelector('button')!,
    );
    await screen.findByDisplayValue('C:\\other\\minions');
    fireEvent.click(screen.getByRole('button', { name: 'Save and restart' }));
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Invalid image root.',
    );
    expect(apply).toHaveBeenCalledWith({
      ...paths,
      minionRoot: 'C:\\other\\minions',
    });
    expect(onClose).not.toHaveBeenCalled();
  });

  it('announces restart and prevents further changes after saving', async () => {
    apply.mockResolvedValue({ ok: true, data: { restarting: true } });
    render(<Settings onClose={onClose} />);
    await screen.findByDisplayValue(paths.databasePath);
    fireEvent.click(screen.getByRole('button', { name: 'Save and restart' }));
    await waitFor(() =>
      expect(screen.getByRole('status')).toHaveTextContent('Restarting'),
    );
    expect(screen.getByRole('button', { name: 'Cancel' })).toBeDisabled();
  });
});
