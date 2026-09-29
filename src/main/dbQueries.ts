import { MinionQuery } from '../constants/dbIpc';
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

function whereQuery(query: MinionQuery): SqlQuery {
  const clauses: string[] = [];
  const params: SqlValue[] = [];

  if (query.ids) {
    clauses.push(`id in (${placeholders(query.ids.length)})`);
    params.push(...query.ids);
  }
  if (query.episodes) {
    clauses.push(`episode in (${placeholders(query.episodes.length)})`);
    params.push(...query.episodes);
  }
  if (query.scenes) {
    clauses.push(`scene in (${placeholders(query.scenes.length)})`);
    params.push(...query.scenes);
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
  const where = whereQuery(query);
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
         select id, url, episode, scene
         from ${query.view}
         limit ? offset ?
      `,
      params: pagination,
    };
  }

  if (query.cards) {
    return {
      statement: `
         select id, url, episode, scene
         from (
           select id, url, episode, scene from ${DB_TABLES.MINIONS} m
           join minion_card_relations mcr on m.id = mcr.minion_id
           where mcr.card_id in (${placeholders(query.cards.length)})
           ${query.rel ? 'and rel = ?' : ''}
         )
         ${where.statement}
         limit ? offset ?
      `,
      params: [
        ...query.cards,
        ...(query.rel ? [query.rel] : []),
        ...where.params,
        ...pagination,
      ],
    };
  }

  return {
    statement: `
      select id, url, episode, scene
      from ${DB_TABLES.MINIONS} ${where.statement}
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
  const where = whereQuery(query);
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

  if (query.cards) {
    return {
      statement: `
         select count(1) as total
         from (
           select id from ${DB_TABLES.MINIONS} m
           join minion_card_relations mcr on m.id = mcr.minion_id
           where mcr.card_id in (${placeholders(query.cards.length)})
           ${query.rel ? 'and rel = ?' : ''}
         )
         ${where.statement}
         limit ? offset ?
      `,
      params: [
        ...query.cards,
        ...(query.rel ? [query.rel] : []),
        ...where.params,
        ...pagination,
      ],
    };
  }

  return {
    statement: `
      select count(1) as total
      from ${DB_TABLES.MINIONS} ${where.statement}
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
