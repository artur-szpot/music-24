import '@testing-library/jest-dom';
import { fireEvent, render, screen } from '@testing-library/react';
import { SCREEN_TYPES } from '../enums/screens';
import { navTo } from '../renderer/interfaces/setScreenProps';
import { MinionDetails } from '../renderer/screens/MinionDetails';

describe('MinionDetails', () => {
  it('shows season, episode, and scene links to filtered minion lists', async () => {
    const minions = jest.fn().mockResolvedValue({
      ok: true,
      data: [
        {
          id: 42,
          url: 'image.png',
          episode: 7,
          scene: 11,
          season: 2,
        },
      ],
    });
    const setScreen = jest.fn();
    window.electron = {
      config: {
        get: jest.fn().mockResolvedValue({
          ok: true,
          data: {
            databasePath: 'C:\\data\\collection.db',
            minionRoot: 'C:\\images\\minions',
            cardRoot: 'C:\\images\\cards',
            fileSystemRoot: 'C:\\images\\files',
            outputDirectory: 'C:\\images\\output',
          },
        }),
        choose: jest.fn(),
        apply: jest.fn(),
      },
      database: {
        labels: jest.fn(),
        categories: jest.fn(),
        cards: jest.fn(),
        minions,
        minionCount: jest.fn(),
        updateCardFilter: jest.fn(),
        minionCards: jest.fn().mockResolvedValue({
          ok: true,
          data: [
            {
              id: 8,
              name: 'Selected card',
              parent: null,
              category: 'Fixture',
              cardType: 'fixture',
              isSelected: 1,
            },
            {
              id: 9,
              name: 'Parent card',
              parent: null,
              category: 'Fixture',
              cardType: 'fixture',
              isSelected: 0,
            },
          ],
        }),
        minionSource: jest.fn().mockResolvedValue({
          ok: true,
          data: {
            fileName: 'image.png',
            fullPath: 'C:\\images\\minions\\7\\image.png',
          },
        }),
        revealMinion: jest.fn().mockResolvedValue({ ok: true, data: true }),
        copyMinion: jest.fn().mockResolvedValue({ ok: true, data: true }),
        cardSubs: jest.fn().mockResolvedValue({ ok: true, data: [] }),
        createCard: jest.fn(),
        renameCard: jest.fn(),
        deleteCard: jest.fn(),
      },
    };

    render(
      <MinionDetails
        id={42}
        screenType={SCREEN_TYPES.SCREEN}
        globalLabels={{
          cards: {},
          episodes: { 7: 'Episode Seven' },
          scenes: { 11: 'Scene Eleven' },
          seasons: { 2: 'Season Two' },
        }}
        handleNav={{ setScreen, setPopup: jest.fn() }}
      />,
    );

    const metadata = await screen.findByRole('group', {
      name: 'Minion metadata',
    });
    expect(metadata).toHaveStyle({ flexWrap: 'nowrap', overflowX: 'auto' });
    expect(await screen.findByText('1 cards selected')).toBeInTheDocument();
    expect(screen.getByText('Selected card (selected)')).toBeInTheDocument();
    expect(screen.getByText('Parent card (parent)')).toBeInTheDocument();
    expect(
      await screen.findByText('C:\\images\\minions\\7\\image.png'),
    ).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Season: Season Two' }));
    fireEvent.click(
      screen.getByRole('button', { name: 'Episode: Episode Seven' }),
    );
    fireEvent.click(
      screen.getByRole('button', { name: 'Scene: Scene Eleven' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Show in Explorer' }));
    fireEvent.click(screen.getByRole('button', { name: 'Copy to output' }));

    expect(setScreen).toHaveBeenNthCalledWith(
      1,
      navTo.minionList({ query: { seasons: [2] } }),
    );
    expect(window.electron.database.revealMinion).toHaveBeenCalledWith(42);
    expect(window.electron.database.copyMinion).toHaveBeenCalledWith(42);
    expect(await screen.findByRole('status')).toHaveTextContent(
      'Copied to output directory.',
    );
    expect(setScreen).toHaveBeenNthCalledWith(
      2,
      navTo.minionList({ query: { episodes: [7] } }),
    );
    expect(setScreen).toHaveBeenNthCalledWith(
      3,
      navTo.minionList({ query: { scenes: [11] } }),
    );
  });
});
