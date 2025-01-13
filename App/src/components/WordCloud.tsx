import React from 'react';

interface WordCloudProps {
  words: Array<{
    text: string;
    value: number;
  }>;
}

export const WordCloud: React.FC<WordCloudProps> = ({ words }) => {
  const maxValue = Math.max(...words.map(word => word.value));
  
  return (
    <div className="p-8 flex flex-wrap gap-4 justify-center items-center min-h-[400px] bg-white rounded-lg shadow-lg">
      {words.map((word, index) => {
        const fontSize = Math.max(1, (word.value / maxValue) * 4); // Scale from 1rem to 4rem
        
        return (
          <span
            key={index}
            className="transition-all duration-300 hover:text-blue-600 cursor-pointer"
            style={{
              fontSize: `${fontSize}rem`,
              opacity: 0.3 + (word.value / maxValue) * 0.7,
              transform: `rotate(${Math.random() * 20 - 10}deg)`,
            }}
          >
            {word.text}
          </span>
        );
      })}
    </div>
  );
};