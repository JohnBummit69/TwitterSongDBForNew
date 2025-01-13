import React, { useState, useEffect } from 'react';
import { WordCloud } from './components/WordCloud';
import { Music, Users, Disc, Upload } from 'lucide-react';
import { UserAnalysis } from './components/UserAnalysis';

// Try to import the data, but it might fail if the file doesn't exist
let musicData: Array<{
  date_created: string;
  username: string;
  song: string;
  artist: string;
  real_nigga?: string;
}> = [];

try {
  musicData = require('./music_datacloud.json');
} catch (error) {
  console.warn('Could not load music data JSON file');
}

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
    if (musicData.length === 0) return;

    const processedWords = [...new Set([
      ...musicData.map(item => item.song),
      ...musicData.map(item => item.artist)
    ])].map(text => {
      const count = musicData.filter(item => 
        item.song === text || item.artist === text
      ).length;
      return {
        text,
        value: count * 10
      };
    }).sort((a, b) => b.value - a.value);

    setWords(processedWords);
  }, []);

  if (musicData.length === 0) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-lg text-center max-w-md">
          <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h2 className="text-2xl font-bold mb-4">No Music Data Available</h2>
          <p className="text-gray-600 mb-4">
            Please provide the music data JSON file to continue. The file should be named 'music_datacloud.json' and placed in the src directory.
          </p>
        </div>
      </div>
    );
  }

  const renderContent = () => {
    switch (currentView) {
      case 'usernames':
        return <UserAnalysis data={musicData} />;
      case 'songs':
        return (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4">Song List</h2>
            <div className="space-y-2">
              {[...new Set(musicData.map(item => item.song))].map((song, index) => (
                <div key={index} className="p-3 bg-gray-50 rounded-md hover:bg-gray-100">
                  <p className="font-medium">{song}</p>
                  <p className="text-sm text-gray-600">
                    {musicData.find(item => item.song === song)?.artist}
                  </p>
                </div>
              ))}
            </div>
          </div>
        );
      default:
        return <WordCloud words={words} />;
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
                Word Cloud
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
                Songs
              </button>
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