import React, { useState, useEffect } from 'react';
import { WordCloud } from './components/WordCloud';
import { Music, Users, Disc, PlusCircle } from 'lucide-react';
import { UserAnalysis } from './components/UserAnalysis';
import { MusicEntry } from './utils/convertData';
import musicDataJson from './music_datacloud.json';

const musicData: MusicEntry[] = musicDataJson;

type View = 'wordcloud' | 'usernames' | 'songs';

function App() {
  const [words, setWords] = useState<Array<{ text: string; value: number }>>([]);
  const [currentView, setCurrentView] = useState<View>('wordcloud');
  const [scrollPosition, setScrollPosition] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScrollPosition(window.scrollY);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    // Count song frequencies
    const songFrequencies = musicData.reduce((acc, item) => {
      const song = item.song_name.trim();
      if (song) {
        acc[song] = (acc[song] || 0) + 1;
      }
      return acc;
    }, {} as Record<string, number>);

    // Convert to word cloud format and sort by frequency
    const processedWords = Object.entries(songFrequencies)
      .map(([text, count]) => ({
        text,
        value: count * 20 // Increased multiplier for better visibility
      }))
      .sort((a, b) => b.value - a.value);

    setWords(processedWords);
  }, []);

  const renderContent = () => {
    switch (currentView) {
      case 'usernames':
        return <UserAnalysis data={musicData} />;
      case 'songs':
        return (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4">Song List</h2>
            <div className="space-y-2">
              {[...new Set(musicData.map(item => item.song_name))].map((song, index) => (
                <div key={index} className="p-3 bg-gray-50 rounded-md hover:bg-gray-100">
                  <p className="font-medium">{song}</p>
                  <p className="text-sm text-gray-600">
                    {musicData.find(item => item.song_name === song)?.artist_name}
                  </p>
                </div>
              ))}
            </div>
          </div>
        );
      default:
        return (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4">Most Played Songs</h2>
            <WordCloud words={words} />
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className={`sticky top-0 z-50 bg-white shadow-md transition-all ${
        scrollPosition > 0 ? 'py-2' : 'py-4'
      }`}>
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex items-center justify-between">
            <h1 className={`font-bold transition-all ${
              scrollPosition > 0 ? 'text-xl' : 'text-2xl'
            }`}>
              Music Collection
            </h1>
            <div className="flex gap-2">
              <button
                onClick={() => setCurrentView('wordcloud')}
                className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
                  currentView === 'wordcloud'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                <Music size={20} />
                Popular Songs
              </button>
              <button
                onClick={() => setCurrentView('usernames')}
                className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
                  currentView === 'usernames'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                <Users size={20} />
                User Analysis
              </button>
              <button
                onClick={() => setCurrentView('songs')}
                className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
                  currentView === 'songs'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                <Disc size={20} />
                All Songs
              </button>
              <a
                href="https://forms.gle/24tmYVi5r69mkbgf7"
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 rounded-lg flex items-center gap-2 bg-green-600 text-white hover:bg-green-700 transition-colors"
              >
                <PlusCircle size={20} />
                Submit Song
              </a>
            </div>
          </div>
        </div>
      </nav>

      <div className="p-8">
        <div className="max-w-4xl mx-auto space-y-8">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

export default App;