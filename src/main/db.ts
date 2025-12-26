import Database from 'better-sqlite3';
import { DB_OPERATIONS, DB_TABLES } from '../enums/db';
import { LIMITS } from '../constants/limits';

const db = new Database('E:\\programming\\ponypics\\year45.db');
db.pragma('journal_mode = WAL');

interface Query {
  statement: string;
  params?: any[];
}

export function dbOperation(args: any) {
  const { operation } = args;
  switch (operation) {
    case DB_OPERATIONS.GET_COUNT:
      const { table } = args;
      return getAll({ statement: `select count(1) from ${table}` });
    case DB_OPERATIONS.GET_MINION:
      const { id } = args;
      return getAll({
        statement: `select id, url, episode, scene from ${DB_TABLES.MINIONS} where id = ${id}`,
      });
    case DB_OPERATIONS.GET_MINIONS:
      return getAll(minionListQuery(args));
    case DB_OPERATIONS.GET_MINIONS_COUNT:
      return getAll(minionListQueryCount(args));
    default:
      throw new Error(`Operation not implemented for ${args[0]}`);
  }
}

function getAll(query: Query) {
  const { statement, params } = query;
  console.log(`Execute SQL: ${statement}`);
  const retval = db.prepare(statement).all(...(params ?? []));
  console.log(`Rows returned: ${retval.length}`);
  if (retval.length > 0) {
    console.log(`Row 0: ${JSON.stringify(retval[0])}`);
    //  console.log(`Row 0 url: ${JSON.stringify(retval[0].url)}`);
  }
  return retval;
}

function minionListQueryCount(args: any): Query {
  const where = minionListQueryWhere(args);
  const statement = `select count(1) from ${DB_TABLES.MINIONS} ${where.statement}`;
  return { statement, params: where.params };
}

function minionListQuery(args: any, page: number = 0): Query {
  const where = minionListQueryWhere(args);
  const statement = `select id, url, episode, scene from ${DB_TABLES.MINIONS} ${where.statement} limit ${LIMITS.MINIONS_PER_PAGE} offset ${page * LIMITS.MINIONS_PER_PAGE}`;
  return { statement, params: where.params };
}

function minionListQueryWhere(args: any): Query {
  const { episodes } = args;
  const where: string[] = [];
  const params: any[] = [];
  if (episodes) {
    where.push(`episode in (${episodes.map(() => '?').join(', ')})`);
    params.push(...episodes);
  }
  if (where.length) {
    return { statement: ` where ${where.join(' and ')}`, params };
  }
  return { statement: '' };
}
