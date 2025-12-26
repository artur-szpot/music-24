import { useCallback, useState } from 'react';
import { DB_OPERATIONS } from '../../enums/db';
import { Minion } from '../components/Minion';

const QUERY_CHANNEL = 'query-channel';

export function Hello() {
  const [data, setData] = useState([] as any[]);

  window.electron.ipcRenderer.once(QUERY_CHANNEL, (arg) => {
    console.log(`Data received: ${JSON.stringify(arg)}`);
    setData(arg as any[]);
  });

  const fetchData = useCallback(() => {
    window.electron.ipcRenderer.sendMessage(QUERY_CHANNEL, {
      operation: DB_OPERATIONS.GET_MINION,
      id: 666,
    });
  }, []);

  if (!data || data.length === 0) {
    fetchData();

    return (
      <div className="screen">
        <img
          height="100px"
          src="file-system:///ed89f8782a61929f6bbd0878c5adad48.png"
        />
      </div>
    );
  }

  return <Minion {...data[0]} />;
}
