import React, { useState, useRef } from 'react';
import SearchBar from './components/SearchBar';
import ResultsGrid from './components/ResultsGrid';
import ProgressBar from './components/ProgressBar'; // Import the new component
import { streamSearch } from './api/searchApi'; // Import the new API function

function App() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  // New state for progress tracking
  const [progress, setProgress] = useState(0);
  const [progressStep, setProgressStep] = useState('');
  
  // Ref to hold the active EventSource connection
  const eventSourceRef = useRef(null);

  const handleSearch = (query) => {
    // If a search is already in progress, cancel it
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    // Reset all state for the new search
    setIsLoading(true);
    setError('');
    setResults([]);
    setProgress(0);
    setProgressStep('');

    eventSourceRef.current = streamSearch(query, {
      onProgress: (update) => {
        setProgress(update.progress);
        setProgressStep(update.step);
      },
      onResults: (finalResults) => {
        setResults(finalResults);
        setIsLoading(false); // Search is complete
      },
      onError: (errorMessage) => {
        setError(errorMessage);
        setIsLoading(false); // Search has failed
      },
    });
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Vicky Visual Search</h1>
        <p>Your AI-Powered Enterprise Image Search</p>
      </header>
      <main>
        <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        
        {/* Conditionally render the progress bar OR the results */}
        {isLoading ? (
          <ProgressBar progress={progress} step={progressStep} />
        ) : (
          results && <ResultsGrid results={results} error={error} />
        )}
      </main>
      <footer className="app-footer">
        <p>&copy; 2025 Vicky Visual Search Inc.</p>
      </footer>
    </div>
  );
}

export default App;