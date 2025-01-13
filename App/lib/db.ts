import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import duckdb_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';

let db: duckdb.AsyncDuckDB | null = null;
let conn: duckdb.AsyncDuckDBConnection | null = null;

export async function initDB() {
  if (db) return db;

  const DUCKDB_CONFIG: duckdb.DuckDBBundles = {
    mvp: {
      mainModule: duckdb_wasm,
      mainWorker: duckdb_worker,
    },
  };

  const bundle = await duckdb.selectBundle(DUCKDB_CONFIG);
  const worker = new Worker(bundle.mainWorker!);
  const logger = new duckdb.ConsoleLogger();
  db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);

  try {
    await db.registerFileURL('music.db', '/music.db');
    await db.open('music.db');
  } catch (error) {
    console.warn('Could not load music.db, creating new database');
  }

  conn = await db.connect();
  return db;
}

export async function getWords() {
  if (!conn) await initDB();
  
  // Query to get songs and artists, count their occurrences for the word cloud
  const result = await conn!.query(`
    SELECT 
      text,
      COUNT(*) * 10 as value
    FROM (
      SELECT song as text FROM songs
      UNION ALL
      SELECT artist as text FROM songs
    ) combined
    GROUP BY text
    ORDER BY value DESC
  `);

  return result.toArray().map(row => ({
    text: row.text,
    value: Number(row.value)
  }));
}

// We don't need these functions anymore since we're reading directly from the songs table
export async function addWord(text: string, value: number) {
  console.warn('Adding words manually is disabled when using the music database');
}

export async function loadJSONData(data: Array<{ text: string, value: number }>) {
  console.warn('Loading JSON data is disabled when using the music database');
}
