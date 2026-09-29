import Database from 'better-sqlite3';
import { executeQuery } from '../main/db';
import { SqlQuery } from '../main/dbQueries';

describe('database query execution', () => {
  it('passes SQL values as bound parameters and returns rows', () => {
    const rows = [{ id: 7 }];
    const all = jest.fn().mockReturnValue(rows);
    const prepare = jest.fn().mockReturnValue({ all });
    const database = { prepare } as unknown as Pick<
      Database.Database,
      'prepare'
    >;
    const query: SqlQuery = {
      statement: 'select id from minions where id = ?',
      params: [7],
    };

    expect(executeQuery(database, query)).toBe(rows);
    expect(prepare).toHaveBeenCalledWith(query.statement);
    expect(all).toHaveBeenCalledWith(7);
  });
});
