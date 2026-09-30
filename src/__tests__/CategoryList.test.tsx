import '@testing-library/jest-dom';
import { fireEvent, render, screen } from '@testing-library/react';
import { SCREEN_TYPES } from '../enums/screens';
import { CategoryList } from '../renderer/screens/CategoryList';

const rows = [
  { id: 1, name: 'Alpha tag', parent: null, category: 'Alpha', total: 2 },
  { id: 2, name: 'Alpha sub', parent: 1, category: 'Alpha', total: 1 },
  { id: 3, name: 'Beta tag', parent: null, category: 'Beta', total: 3 },
];

const summaryFor = (label: string) =>
  screen.getByText(label).closest('.MuiAccordionSummary-root') as HTMLElement;

describe('CategoryList accordions', () => {
  beforeEach(() => {
    window.electron = {
      config: { get: jest.fn(), choose: jest.fn(), apply: jest.fn() },
      database: {
        labels: jest.fn(),
        categories: jest.fn().mockResolvedValue({ ok: true, data: rows }),
        cards: jest.fn(),
        minions: jest.fn(),
        minionCount: jest.fn(),
        updateCardFilter: jest.fn(),
        minionCards: jest.fn(),
        minionSource: jest.fn(),
        revealMinion: jest.fn(),
        copyMinion: jest.fn(),
        cardSubs: jest.fn(),
        createCard: jest.fn(),
        renameCard: jest.fn(),
        deleteCard: jest.fn(),
      },
    };
  });

  const renderList = () =>
    render(
      <CategoryList
        dbOperation="tags"
        screenType={SCREEN_TYPES.SCREEN}
        actions={[]}
        navActions={[]}
        globalLabels={{ cards: {}, episodes: {}, scenes: {}, seasons: {} }}
        handleNav={{ setScreen: jest.fn(), setPopup: jest.fn() }}
      />,
    );

  it('opens one top-level category at a time', async () => {
    renderList();
    await screen.findByText('Alpha');

    fireEvent.click(summaryFor('Alpha'));
    expect(summaryFor('Alpha')).toHaveAttribute('aria-expanded', 'true');

    fireEvent.click(summaryFor('Beta'));
    expect(summaryFor('Beta')).toHaveAttribute('aria-expanded', 'true');
    expect(summaryFor('Alpha')).toHaveAttribute('aria-expanded', 'false');

    fireEvent.click(summaryFor('Beta'));
    expect(summaryFor('Beta')).toHaveAttribute('aria-expanded', 'false');
  });

  it('expands a nested tag independently of its category', async () => {
    renderList();
    await screen.findByText('Alpha');

    fireEvent.click(summaryFor('Alpha'));
    fireEvent.click(summaryFor('Alpha tag'));

    expect(summaryFor('Alpha tag')).toHaveAttribute('aria-expanded', 'true');
    expect(summaryFor('Alpha')).toHaveAttribute('aria-expanded', 'true');
  });

  it('offers no expand control for tags without subs', async () => {
    renderList();
    await screen.findByText('Alpha');

    expect(
      summaryFor('Alpha tag').querySelector('[data-testid="ExpandMoreIcon"]'),
    ).not.toBeNull();
    expect(
      summaryFor('Alpha sub').querySelector('[data-testid="ExpandMoreIcon"]'),
    ).toBeNull();

    fireEvent.click(summaryFor('Alpha sub'));
    expect(summaryFor('Alpha sub')).toHaveAttribute('aria-expanded', 'false');
  });
});
