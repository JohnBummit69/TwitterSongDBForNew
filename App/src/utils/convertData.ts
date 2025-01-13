export interface MusicEntry {
  date_created: string;
  username: string;
  song_name: string;
  artist_name: string;
}

export function convertArrayToJSON(data: any[]): MusicEntry[] {
  return data
    .filter(entry => entry.username && entry.song_name && entry.artist_name) // Remove empty entries
    .map(entry => ({
      date_created: entry.Timestamp || new Date().toISOString(),
      username: entry.username.trim(),
      song_name: entry.song_name.toString().trim(), // Convert to string in case of numbers
      artist_name: entry.artist_name.trim()
    }));
}
