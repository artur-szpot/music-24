import { FilterCategory, MinionFilter, MinionQuery } from '../constants/dbIpc';
import { LIMITS } from '../constants/limits';
import { DB_OPERATIONS, DB_TABLES } from '../enums/db';
import { DbRequest } from './dbHandlers';

export type SqlValue = number | string;

export interface SqlQuery {
  statement: string;
  params: SqlValue[];
}

function emptyParams(statement: string): SqlQuery {
  return { statement, params: [] };
}

function placeholders(count: number): string {
  return Array.from({ length: count }, () => '?').join(', ');
}

function filterPredicate(filter: MinionFilter, minionAlias: string): SqlQuery {
  const clauses: string[] = [];
  const params: SqlValue[] = [];

  const addCategory = (
    category: FilterCategory | undefined,
    kind: 'cards' | 'seasons' | 'episodes' | 'scenes',
  ) => {
    if (!category) return;
    const categoryClauses: string[] = [];
    (['oneOf', 'allOf', 'noneOf'] as const).forEach((operator) => {
      const values = category[operator];
      if (!values?.length) return;
      const valuePlaceholders = Array.from(
        { length: values.length },
        () => '?',
      ).join(', ');

      if (kind === 'cards') {
        if (operator === 'oneOf') {
          categoryClauses.push(
            `exists (select 1 from minion_card_relations mcr where mcr.minion_id = ${minionAlias}.id and mcr.card_id in (${valuePlaceholders}))`,
          );
          params.push(...values);
        } else if (operator === 'allOf') {
          categoryClauses.push(
            `(select count(distinct mcr.card_id) from minion_card_relations mcr where mcr.minion_id = ${minionAlias}.id and mcr.card_id in (${valuePlaceholders})) = ${values.length}`,
          );
          params.push(...values);
        } else {
          categoryClauses.push(
            `not exists (select 1 from minion_card_relations mcr where mcr.minion_id = ${minionAlias}.id and mcr.card_id in (${valuePlaceholders}))`,
          );
          params.push(...values);
        }
        return;
      }

      const column =
        kind === 'episodes'
          ? `${minionAlias}.episode`
          : kind === 'scenes'
            ? `${minionAlias}.scene`
            : undefined;
      const seasonSource = `select id from ${DB_TABLES.EPISODES} where season`;
      if (operator === 'allOf') {
        categoryClauses.push(
          `(${values
            .map(() =>
              column
                ? `${column} = ?`
                : `${minionAlias}.episode in (${seasonSource} = ?)`,
            )
            .join(' and ')})`,
        );
        params.push(...values);
      } else {
        const expression = column ?? `${minionAlias}.episode`;
        const membership = operator === 'noneOf' ? 'not in' : 'in';
        categoryClauses.push(
          kind === 'seasons'
            ? `${expression} ${membership} (${seasonSource} in (${valuePlaceholders}))`
            : `${expression} ${membership} (${valuePlaceholders})`,
        );
        params.push(...values);
      }
    });
    if (categoryClauses.length) {
      clauses.push(`(${categoryClauses.join(' and ')})`);
    }
  };

  addCategory(filter.cards, 'cards');
  addCategory(filter.seasons, 'seasons');
  addCategory(filter.episodes, 'episodes');
  addCategory(filter.scenes, 'scenes');
  (filter.views ?? []).forEach((child) => {
    const nested = filterPredicate(child, minionAlias);
    clauses.push(nested.statement);
    params.push(...nested.params);
  });

  if (!clauses.length) throw new Error('Minion filters need conditions.');
  return {
    statement: `(${clauses.join(filter.logic === 'all' ? ' and ' : ' or ')})`,
    params,
  };
}

function whereQuery(query: MinionQuery, minionAlias: string): SqlQuery {
  const clauses: string[] = [];
  const params: SqlValue[] = [];

  if (query.ids) {
    clauses.push(`${minionAlias}.id in (${placeholders(query.ids.length)})`);
    params.push(...query.ids);
  }
  if (query.episodes) {
    clauses.push(
      `${minionAlias}.episode in (${placeholders(query.episodes.length)})`,
    );
    params.push(...query.episodes);
  }
  if (query.seasons) {
    clauses.push(
      `${minionAlias}.episode in (select id from ${DB_TABLES.EPISODES} where season in (${placeholders(query.seasons.length)}))`,
    );
    params.push(...query.seasons);
  }
  if (query.scenes) {
    clauses.push(
      `${minionAlias}.scene in (${placeholders(query.scenes.length)})`,
    );
    params.push(...query.scenes);
  }
  if (query.cards) {
    clauses.push(
      `exists (select 1 from minion_card_relations mcr where mcr.minion_id = ${minionAlias}.id and mcr.card_id in (${placeholders(query.cards.length)})${query.rel ? ' and mcr.rel = ?' : ''})`,
    );
    params.push(...query.cards, ...(query.rel ? [query.rel] : []));
  }
  if (query.filter) {
    const filter = filterPredicate(query.filter, minionAlias);
    clauses.push(filter.statement);
    params.push(...filter.params);
  }

  return {
    statement: clauses.length ? ` where ${clauses.join(' and ')}` : '',
    params,
  };
}

function minionQuery(
  request: { query: MinionQuery; page?: number },
  allowedViews: readonly string[],
): SqlQuery {
  const { query, page = 0 } = request;
  const where = whereQuery(query, 'm');
  const pagination = [LIMITS.MINIONS_PER_PAGE, page * LIMITS.MINIONS_PER_PAGE];

  if (query.view) {
    if (
      !/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(query.view) ||
      !allowedViews.includes(query.view)
    ) {
      throw new Error('Unknown database view.');
    }
    return {
      statement: `
        select v.id, v.url, v.episode, v.scene, e.season
        from ${query.view} v
        left join ${DB_TABLES.EPISODES} e on e.id = v.episode
         ${query.random ? 'order by random()' : ''}
         limit ? offset ?
      `,
      params: pagination,
    };
  }

  return {
    statement: `
      select m.id, m.url, m.episode, m.scene,
        (select season from ${DB_TABLES.EPISODES} e where e.id = m.episode) as season
      from ${DB_TABLES.MINIONS} m ${where.statement}
      ${query.random ? 'order by random()' : ''}
      limit ? offset ?
    `,
    params: [...where.params, ...pagination],
  };
}

function minionCountQuery(
  request: { query: MinionQuery; page?: number },
  allowedViews: readonly string[],
): SqlQuery {
  const { query, page = 0 } = request;
  const where = whereQuery(query, 'm');
  const pagination = [LIMITS.MINIONS_PER_PAGE, page * LIMITS.MINIONS_PER_PAGE];

  if (query.view) {
    if (
      !/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(query.view) ||
      !allowedViews.includes(query.view)
    ) {
      throw new Error('Unknown database view.');
    }
    return {
      statement: `
         select count(1) as total
         from ${query.view}
         limit ? offset ?
      `,
      params: pagination,
    };
  }

  return {
    statement: `
      select count(1) as total
      from ${DB_TABLES.MINIONS} m ${where.statement}
      limit ? offset ?
    `,
    params: [...where.params, ...pagination],
  };
}

export function buildDbQuery(
  request: DbRequest,
  allowedViews: readonly string[] = [],
): SqlQuery {
  switch (request.operation) {
    case DB_OPERATIONS.GET_MINIONS:
      return minionQuery(request, allowedViews);
    case DB_OPERATIONS.GET_MINIONS_COUNT:
      return minionCountQuery(request, allowedViews);
    case DB_OPERATIONS.GET_TAG_CATEGORIES:
      return emptyParams(`
         select id, name, parent, category, coalesce(total, 0) as total from (
          select id, name, parent, category, total from ${DB_TABLES.CARDS} c
          join minion_card_relations_counts mcr
          on c.id = mcr.card_id
          where card_type <> 'combined' and category <> 'technical'
         )
      `);
    case DB_OPERATIONS.GET_EPISODES:
      return emptyParams(`
         select id, name, CASE WHEN season = 0 THEN 'Other' ELSE 'Season ' || season END AS category, null as parent, coalesce(total, 0) as total from (
          select id, e.episode, e.episode || '. ' || name as name, season, total from ${DB_TABLES.EPISODES} e
          join minion_episodes_counts me
          on e.id = me.episode
         )
         order by season asc, episode asc
      `);
    case DB_OPERATIONS.GET_SCENES:
      return emptyParams(`
       select name, id, episode * -1 as parent, null as episode, CASE WHEN season = 0 THEN 'Other' ELSE 'Season ' || season END AS category, coalesce(total, 0) as total from (
          select s.name, s.id, s.episode, e.season, total from ${DB_TABLES.SCENES} s
          join episodes e
          on s.episode = e.id
          join minion_scenes_counts ms
          on s.id = ms.scene
       ) ss
       union all
       select name, id * -1 as id, null as parent, episode, CASE WHEN season = 0 THEN 'Other' ELSE 'Season ' || season END AS category, coalesce(total, 0) as total from (
          select id, e.episode, e.episode || '. ' || name as name, season, total from ${DB_TABLES.EPISODES} e
          join minion_episodes_counts me
          on e.id = me.episode
       )
       order by category asc, episode asc, id asc
      `);
    case DB_OPERATIONS.GET_IMPLEMENTATION_CATEGORIES:
      return emptyParams(`
         select id, name, parent, category, coalesce(total, 0) as total from (
          select id, name, parent, category, total from ${DB_TABLES.CARDS} c
          join minion_card_relations_counts mcr
          on c.id = mcr.card_id
          where card_type = 'combined' and mcr.rel = 'p'
         )
      `);
    case DB_OPERATIONS.GET_CARDS:
      return {
        statement: `
           select id, name, parent, category, card_type as cardType, view
           from ${DB_TABLES.CARDS} c
           where id in (${placeholders(request.query.ids.length)})
        `,
        params: request.query.ids,
      };
    case DB_OPERATIONS.UPDATE_CARD_FILTER:
      return {
        statement: `update ${DB_TABLES.CARDS} set view = ? where id = ?`,
        params: [JSON.stringify(request.filter), request.cardId],
      };
    case DB_OPERATIONS.GET_MINION_CARDS:
      return {
        statement: `
          with recursive selected_cards as (
            select distinct c.id, c.name, c.parent, c.category,
              c.card_type as cardType
            from minion_card_relations mcr
            join ${DB_TABLES.CARDS} c on c.id = mcr.card_id
            where mcr.minion_id = ?
          ), card_tree(id, name, parent, category, cardType, isSelected) as (
            select id, name, parent, category, cardType, 1
            from selected_cards
            union
            select parent_card.id, parent_card.name, parent_card.parent,
              parent_card.category, parent_card.card_type, 0
            from ${DB_TABLES.CARDS} parent_card
            join card_tree child on parent_card.id = child.parent
          )
          select id, name, parent, category, cardType,
            max(isSelected) as isSelected
          from card_tree
          group by id, name, parent, category, cardType
          order by isSelected desc, category asc, name asc
        `,
        params: [request.minionId],
      };
    case DB_OPERATIONS.INITIALIZE_LABELS:
      return emptyParams(`
         select id, name, 'card' as category from ${DB_TABLES.CARDS}
         union all
         select id, name, 'scene' as category from ${DB_TABLES.SCENES}
         union all
         select id, name, 'episode' as category from ${DB_TABLES.EPISODES}
      `);
    default:
      throw new Error('Operation not implemented.');
  }
}
