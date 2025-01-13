import React from 'react';
import { User, Check, X } from 'lucide-react';

interface MusicData {
  date_created: string;
  username: string;
  song: string;
  artist: string;
  real_nigga?: string;
}

interface UserAnalysisProps {
  data: MusicData[];
}

export const UserAnalysis: React.FC<UserAnalysisProps> = ({ data }) => {
  const userStats = React.useMemo(() => {
    const stats = new Map<string, {
      songCount: number;
      artists: Set<string>;
      isReal: boolean;
      firstSeen: string;
      lastSeen: string;
    }>();

    data.forEach(entry => {
      const current = stats.get(entry.username) || {
        songCount: 0,
        artists: new Set<string>(),
        isReal: entry.real_nigga === 'true',
        firstSeen: entry.date_created,
        lastSeen: entry.date_created,
      };

      current.songCount++;
      current.artists.add(entry.artist);
      current.firstSeen = entry.date_created < current.firstSeen ? entry.date_created : current.firstSeen;
      current.lastSeen = entry.date_created > current.lastSeen ? entry.date_created : current.lastSeen;

      stats.set(entry.username, current);
    });

    return Array.from(stats.entries()).map(([username, stats]) => ({
      username,
      ...stats,
      artistCount: stats.artists.size,
    }));
  }, [data]);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold flex items-center gap-2">
        <User size={24} />
        User Analysis
      </h2>
      
      <div className="grid gap-4 md:grid-cols-2">
        {userStats.map(user => (
          <div key={user.username} className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold">{user.username}</h3>
              {user.isReal ? (
                <span className="flex items-center gap-1 text-green-600">
                  <Check size={18} />
                  Real
                </span>
              ) : (
                <span className="flex items-center gap-1 text-red-600">
                  <X size={18} />
                  Not Real
                </span>
              )}
            </div>
            
            <div className="space-y-2 text-gray-600">
              <p>Songs Added: {user.songCount}</p>
              <p>Unique Artists: {user.artistCount}</p>
              <p className="text-sm">First Seen: {new Date(user.firstSeen).toLocaleDateString()}</p>
              <p className="text-sm">Last Seen: {new Date(user.lastSeen).toLocaleDateString()}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};