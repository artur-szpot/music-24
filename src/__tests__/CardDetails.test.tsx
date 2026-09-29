import '@testing-library/jest-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { SCREEN_TYPES } from '../enums/screens';
import { navTo } from '../renderer/interfaces/setScreenProps';
import { CardDetails } from '../renderer/screens/CardDetails';

describe('CardDetails', () => {
  it('shows the filter count, navigates to matches, and displays a related representative', async () => {
    const filter = {
      logic: 'all' as const,
      episodes: { oneOf: [7] },
    };
    const representative = {
      id: 42,
      url: 'representative.png',
      episode: 7,
      scene: 11,
      season: 2,
    };
    const minions = jest.fn((query: { cards?: number[] }) =>
      Promise.resolve(
        query.cards
          ? { ok: true as const, data: [representative] }
          : { ok: true as const, data: [] },
      ),
    );
    const minionCount = jest.fn().mockResolvedValue({ ok: true, data: 2 });
    const updateCardFilter = jest
      .fn()
      .mockResolvedValue({ ok: true, data: true });
    const setScreen = jest.fn();
    const setPopup = jest.fn();
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
        labels: jest.fn(),
        categories: jest.fn(),
        cards: jest.fn().mockResolvedValue({
          ok: true,
          data: [
            {
              id: 9,
              name: 'Sample card',
              category: 'Sample',
              cardType: 'combined',
              parent: null,
              view: JSON.stringify(filter),
            },
          ],
        }),
        minions,
        minionCount,
        updateCardFilter,
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

    const { container } = render(
      <CardDetails
        id={9}
        screenType={SCREEN_TYPES.SCREEN}
        globalLabels={{
          cards: {},
          episodes: { 7: 'Episode Seven' },
          scenes: { 11: 'Scene Eleven' },
          seasons: { 2: 'Season Two' },
        }}
        handleNav={{ setScreen, setPopup }}
      />,
    );

    expect(
      await screen.findByText('2 minions match this filter.'),
    ).toBeInTheDocument();
    expect(minionCount).toHaveBeenCalledWith({ filter });
    expect(minions).toHaveBeenCalledWith({ cards: [9], random: true }, 0);
    expect(container.querySelector('img')?.getAttribute('src')).toContain(
      'representative.png',
    );

    fireEvent.click(
      screen.getByRole('button', { name: 'View filtered minions' }),
    );
    expect(setScreen).toHaveBeenCalledWith(
      navTo.minionList({ query: { filter } }),
    );

    fireEvent.click(screen.getByRole('button', { name: 'Edit filter' }));
    expect(screen.getByRole('combobox', { name: 'Match' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Save filter' }));
    await waitFor(() =>
      expect(updateCardFilter).toHaveBeenCalledWith(9, filter),
    );
    expect(
      screen.getByRole('button', { name: 'Edit filter' }),
    ).toBeInTheDocument();
  });
});
