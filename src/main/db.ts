import Database from 'better-sqlite3';
import { DB_OPERATIONS, DB_TABLES } from '../enums/db';
import { LIMITS } from '../constants/limits';

const db = new Database('E:\\programming\\ponypics\\year45.db');
db.pragma('journal_mode = WAL');

interface Query {
  statement: string;
  params?: any[];
}

export interface SubCard {
  id: number;
  name: string;
  parent: number | null;
  category: string;
  total: number;
}

export function dbOperation(args: any) {
  const { operation } = args;
  switch (operation) {
    case DB_OPERATIONS.GET_COUNT:
      const { table } = args;
      return getAll({ statement: `select count(1) as total from ${table}` });
    case DB_OPERATIONS.GET_MINION:
      const { id } = args;
      return getAll({
        statement: `select id, url, episode, scene, filter from ${DB_TABLES.MINIONS} where id = ${id}`,
      });
    case DB_OPERATIONS.GET_MINIONS:
      return getAll(minionListQuery(args));
    case DB_OPERATIONS.GET_MINIONS_COUNT:
      return getAll(minionListQueryCount(args));
    case DB_OPERATIONS.GET_TAG_CATEGORIES:
      return getAll({
        statement: `
           select id, name, parent, category, coalesce(total, 0) as total from (
            select id, name, parent, category, total from ${DB_TABLES.CARDS} c
            join minion_card_relations_counts mcr
            on c.id = mcr.card_id
            where card_type <> 'combined' and category <> 'technical'
           )
           `,
      });
    case DB_OPERATIONS.GET_EPISODES:
      return getAll({
        statement: `
           select id, name, CASE WHEN season = 0 THEN 'Other' ELSE 'Season ' || season END AS category, null as parent, coalesce(total, 0) as total from (
            select id, e.episode, e.episode || '. ' || name as name, season, total from ${DB_TABLES.EPISODES} e
            join minion_episodes_counts me
            on e.id = me.episode
           )
           order by season asc, episode asc
           `,
      });
    case DB_OPERATIONS.GET_SCENES:
      return getAll({
        statement: `
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
           `,
      });
    case DB_OPERATIONS.GET_IMPLEMENTATION_CATEGORIES:
      return getAll({
        statement: `
           select id, name, parent, category, coalesce(total, 0) as total from (
            select id, name, parent, category, total from ${DB_TABLES.CARDS} c
            join minion_card_relations_counts mcr
            on c.id = mcr.card_id
            where card_type = 'combined' and mcr.rel = 'p'
           )
           `,
      });
    case DB_OPERATIONS.GET_CARDS:
      const { query } = args;
      const { ids } = query;
      const params: any[] = [];
      params.push(...ids);
      return getAll({
        statement: `
           select id, name, parent, category, card_type as cardType, view
           from ${DB_TABLES.CARDS} c
           where id in (${ids.map(() => '?').join(', ')})
           `,
        params,
      });
    case DB_OPERATIONS.INITIALIZE_LABELS:
      return getAll({
        statement: `
           select id, name, 'card' as category from ${DB_TABLES.CARDS}
           union all
           select id, name, 'scene' as category from ${DB_TABLES.SCENES}
           union all
           select id, name, 'episode' as category from ${DB_TABLES.EPISODES}
           `,
      });
    default:
      throw new Error(`Operation not implemented for ${args[0]}`);
  }
}

function getAll(query: Query) {
  const { statement, params } = query;
  console.log(`Execute SQL: ${statement}`);
  try {
    const retval = db.prepare(statement).all(...(params ?? []));
    console.log(`Rows returned: ${retval.length}`);
    if (retval.length > 0) {
      console.log(`Row 0: ${JSON.stringify(retval[0])}`);
    }
    return retval;
  } catch (e) {
    console.log(`SQL error: ${e}`);
    return [];
  }
}

function minionListQueryCount(args: any): Query {
  const where = minionListQueryWhere(args);
  const { page = 0, query } = args;
  const statement = (({ view, cards, rel }) => {
    if (view) {
      return `
         select count(1) as total
         from ${view} 
         limit ${LIMITS.MINIONS_PER_PAGE} offset ${page * LIMITS.MINIONS_PER_PAGE}
      `;
    }
    if (cards) {
      return `
         select count(1) as total
         from (
           select id from ${DB_TABLES.MINIONS} m
           join minion_card_relations mcr on m.id = mcr.minion_id
           where mcr.card_id in (${cards.map((card: number) => `${card}`).join(', ')})
           ${rel ? `and rel = '${rel}'` : ''}
         )
         ${where.statement} 
         limit ${LIMITS.MINIONS_PER_PAGE} offset ${page * LIMITS.MINIONS_PER_PAGE}
         `;
    }
    return `
      select count(1) as total
      from ${DB_TABLES.MINIONS} ${where.statement} 
      limit ${LIMITS.MINIONS_PER_PAGE} offset ${page * LIMITS.MINIONS_PER_PAGE}
    `;
  })(query);
  return { statement, params: where.params };
}

function minionListQuery(args: any): Query {
  const where = minionListQueryWhere(args);
  const { page = 0, query } = args;
  const statement = (({ view, cards, rel }) => {
    if (view) {
      return `
         select id, url, episode, scene 
         from ${view} 
         limit ${LIMITS.MINIONS_PER_PAGE} offset ${page * LIMITS.MINIONS_PER_PAGE}
      `;
    }
    if (cards) {
      return `
         select id, url, episode, scene 
         from (
           select id, url, episode, scene from ${DB_TABLES.MINIONS} m
           join minion_card_relations mcr on m.id = mcr.minion_id
           where mcr.card_id in (${cards.map((card: number) => `${card}`).join(', ')})
           ${rel ? `and rel = '${rel}'` : ''}
         )
         ${where.statement} 
         limit ${LIMITS.MINIONS_PER_PAGE} offset ${page * LIMITS.MINIONS_PER_PAGE}
         `;
    }
    return `
      select id, url, episode, scene 
      from ${DB_TABLES.MINIONS} ${where.statement} 
      limit ${LIMITS.MINIONS_PER_PAGE} offset ${page * LIMITS.MINIONS_PER_PAGE}
    `;
  })(query);
  return { statement, params: where.params };
}

function minionListQueryWhere(args: any): Query {
  const { query } = args;
  const { episodes, ids, cards, scenes, view } = query;
  const where: string[] = [];
  const params: any[] = [];
  if (ids) {
    where.push(`id in (${ids.map(() => '?').join(', ')})`);
    params.push(...ids);
  }
  if (episodes) {
    where.push(`episode in (${episodes.map(() => '?').join(', ')})`);
    params.push(...episodes);
  }
  if (scenes) {
    where.push(`scene in (${scenes.map(() => '?').join(', ')})`);
    params.push(...scenes);
  }
  if (where.length) {
    return { statement: ` where ${where.join(' and ')}`, params };
  }
  return { statement: '' };
}
