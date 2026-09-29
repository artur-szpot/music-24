import Database from 'better-sqlite3';
import { buildDbQuery, SqlQuery } from './dbQueries';
import { DbRequest } from './dbHandlers';

let db: Database.Database | undefined;

export function initializeDatabase(databasePath: string): void {
  db?.close();
  db = new Database(databasePath);
  db.pragma('journal_mode = WAL');
}

export function viewExists(name: string): boolean {
  if (!db) throw new Error('Database has not been initialized.');
  if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(name)) return false;
  return Boolean(
    db
      .prepare("select 1 from sqlite_master where type = 'view' and name = ?")
      .get(name),
  );
}

export function executeQuery(
  database: Pick<Database.Database, 'prepare'>,
  query: SqlQuery,
) {
  return database.prepare(query.statement).all(...query.params);
}

export function dbOperation(args: DbRequest) {
  if (!db) {
    throw new Error('Database has not been initialized.');
  }
  const requestedView =
    'query' in args && 'view' in args.query ? args.query.view : undefined;
  const allowedViews =
    typeof requestedView === 'string' && viewExists(requestedView)
      ? [requestedView]
      : [];
  return executeQuery(db, buildDbQuery(args, allowedViews));
}
