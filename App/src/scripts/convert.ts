import { readFileSync } from 'fs';
import { join } from 'path';
import { convertArrayToJSON } from '../utils/convertData';
import { saveToJSON } from '../utils/saveData';

// Read the raw data from file
const rawData = JSON.parse(
  readFileSync(join(process.cwd(), 'src', 'raw_data.json'), 'utf-8')
);

// Convert the data
const jsonData = convertArrayToJSON(rawData);

// Save to file
saveToJSON(jsonData);
