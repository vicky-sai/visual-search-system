import React from 'react';
import ImageCard from './ImageCard';

const ResultsGrid = ({ results, isLoading, error }) => {
  if (isLoading) {
    return <div className="status-message">Searching...</div>;
  }

  if (error) {
    return <div className="status-message error">{error}</div>;
  }

  if (results.length === 0) {
    return <div className="status-message">No results found. Try another search.</div>;
  }

  return (
    <div className="results-grid">
      {results.map((item) => (
        <ImageCard
          key={item.image_id}
          imageUrl={item.image_url}
          explanation={item.explanation}
          score={item.score}
        />
      ))}
    </div>
  );
};

export default ResultsGrid;