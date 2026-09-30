import '@testing-library/jest-dom';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { SCREEN_TYPES } from '../enums/screens';
import { navTo } from '../renderer/interfaces/setScreenProps';
import { TagDetails } from '../renderer/screens/TagDetails';

const tree = [
  {
    id: 10,
    name: 'Root tag',
    parent: null,
    category: 'Tags',
    cardType: 'tag',
    total: 1,
    subtreeTotal: 3,
  },
  {
    id: 11,
    name: 'Alpha sub',
    parent: 10,
    category: 'Tags',
    cardType: 'tag',
    total: 1,
    subtreeTotal: 2,
  },
  {
    id: 13,
    name: 'Deep sub',
    parent: 11,
    category: 'Tags',
    cardType: 'tag',
    total: 1,
    subtreeTotal: 1,
  },
];

describe('TagDetails', () => {
  const setScreen = jest.fn();
  const setPopup = jest.fn();
  const cardSubs = jest.fn();
  const createCard = jest.fn();
  const renameCard = jest.fn();
  const deleteCard = jest.fn();

  const renderScreen = () =>
    render(
      <TagDetails
        id={10}
        screenType={SCREEN_TYPES.SCREEN}
        globalLabels={{ cards: {}, episodes: {}, scenes: {}, seasons: {} }}
        handleNav={{ setScreen, setPopup }}
      />,
    );

  beforeEach(() => {
    jest.clearAllMocks();
    cardSubs.mockResolvedValue({ ok: true, data: tree });
    window.electron = {
      config: { get: jest.fn(), choose: jest.fn(), apply: jest.fn() },
      database: {
        labels: jest.fn(),
        categories: jest.fn(),
        cards: jest.fn(),
        minions: jest.fn(),
        minionCount: jest.fn(),
        updateCardFilter: jest.fn(),
        minionCards: jest.fn(),
        minionSource: jest.fn(),
        revealMinion: jest.fn(),
        copyMinion: jest.fn(),
        cardSubs,
        createCard,
        renameCard,
        deleteCard,
      },
    };
  });

  it('lists subs and navigates to direct and subtree image lists', async () => {
    renderScreen();
    expect(await screen.findByRole('heading', { level: 1 })).toHaveTextContent(
      'Root tag',
    );
    expect(screen.getByText('Subs (1)')).toBeInTheDocument();

    fireEvent.click(
      screen.getAllByRole('button', { name: '1 images directly' })[0],
    );
    expect(setScreen).toHaveBeenCalledWith(
      navTo.minionList({ query: { cards: [10], rel: 'p' } }),
    );

    fireEvent.click(
      screen.getByRole('button', { name: '3 images including 2 subs' }),
    );
    expect(setScreen).toHaveBeenCalledWith(
      navTo.minionList({ query: { cards: [10, 11, 13], rel: 'p' } }),
    );

    fireEvent.click(screen.getByRole('button', { name: 'Alpha sub (1 subs)' }));
    expect(setScreen).toHaveBeenCalledWith(navTo.tagDetails({ id: 11 }));
  });

  it('adds a sub and reloads the tree', async () => {
    createCard.mockResolvedValue({ ok: true, data: true });
    renderScreen();
    await screen.findByRole('heading', { level: 1 });

    fireEvent.click(screen.getAllByRole('button', { name: 'Add sub' })[0]);
    fireEvent.change(screen.getByLabelText('New sub name'), {
      target: { value: 'Gamma sub' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Create sub' }));

    await waitFor(() =>
      expect(createCard).toHaveBeenCalledWith(10, 'Gamma sub'),
    );
    await waitFor(() => expect(cardSubs).toHaveBeenCalledTimes(2));
  });

  it('explains why a populated tag cannot be removed', async () => {
    deleteCard.mockResolvedValue({ ok: true, data: false });
    renderScreen();
    await screen.findByRole('heading', { level: 1 });

    fireEvent.click(screen.getAllByRole('button', { name: 'Remove' })[0]);
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Only tags without subs and without images can be removed.',
    );
    expect(setScreen).not.toHaveBeenCalled();
  });

  it('renames a sub through the inline form', async () => {
    renameCard.mockResolvedValue({ ok: true, data: true });
    renderScreen();
    await screen.findByRole('heading', { level: 1 });

    fireEvent.click(screen.getAllByRole('button', { name: 'Rename' })[1]);
    fireEvent.change(screen.getByLabelText('Tag name'), {
      target: { value: 'Alpha renamed' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Save name' }));

    await waitFor(() =>
      expect(renameCard).toHaveBeenCalledWith(11, 'Alpha renamed'),
    );
  });
});
