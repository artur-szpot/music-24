import '@testing-library/jest-dom';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../renderer/App';

describe('App', () => {
  beforeEach(() => {
    window.electron = {
      config: {
        get: jest.fn().mockResolvedValue({
          ok: true,
          data: {
            databasePath: 'C:\\data\\collection.db',
            minionRoot: 'C:\\images\\minions',
            cardRoot: 'C:\\images\\cards',
            fileSystemRoot: 'C:\\images\\files',
          },
        }),
        choose: jest.fn(),
        apply: jest.fn(),
      },
      database: {
        labels: jest.fn().mockResolvedValue({ ok: true, data: [] }),
        categories: jest.fn(),
        cards: jest.fn(),
        minions: jest.fn().mockResolvedValue({ ok: true, data: [] }),
        minionCount: jest.fn().mockResolvedValue({ ok: true, data: 0 }),
        updateCardFilter: jest.fn(),
        minionCards: jest.fn().mockResolvedValue({ ok: true, data: [] }),
        minionSource: jest.fn().mockResolvedValue({
          ok: false,
          error: {
            code: 'NOT_FOUND',
            message: 'Minion source file was not found.',
          },
        }),
        revealMinion: jest.fn(),
        copyMinion: jest.fn(),
      },
    };
  });

  it('renders after loading labels', async () => {
    render(<App />);
    await waitFor(() =>
      expect(screen.queryAllByText('Loading...')).toHaveLength(0),
    );
    expect(
      screen.getByRole('button', { name: 'Settings' }),
    ).toBeInTheDocument();
  });

  it('keeps settings accessible when labels fail', async () => {
    (window.electron.database.labels as jest.Mock).mockResolvedValueOnce({
      ok: false,
      error: { code: 'DATABASE_ERROR', message: 'Could not load data.' },
    });
    render(<App />);
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Could not load data.',
    );
    expect(
      screen.getByRole('button', { name: 'Settings' }),
    ).toBeInTheDocument();
  });
});
