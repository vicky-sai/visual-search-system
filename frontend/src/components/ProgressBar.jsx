import React from 'react';

const ProgressBar = ({ progress, step }) => {
  return (
    <div className="progress-container">
      <div className="progress-bar-track">
        <div
          className="progress-bar-fill"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <p className="progress-step">{step}</p>
    </div>
  );
};

export default ProgressBar;