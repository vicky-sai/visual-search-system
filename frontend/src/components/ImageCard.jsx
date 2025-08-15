import React from 'react';

// Accept 'score' as a new prop
const ImageCard = ({ imageUrl, explanation, score }) => {
  return (
    <div className="image-card">
      <div className="score-badge">{score}% Match</div>
      <img src={imageUrl} alt="Search result" className="result-image" />
      <div className="explanation-box">
        <p className="explanation-text">{explanation}</p>
      </div>
    </div>
  );
};

export default ImageCard;