// The base URL for our FastAPI backend
const API_URL = 'http://localhost:8000/api/v1';

/**
 * Performs a streaming search.
 * @param {string} queryText - The text to search for.
 * @param {Function} onProgress - Callback for progress updates.
 * @param {Function} onResults - Callback for the final results.
 * @param {Function} onError - Callback for errors.
 * @returns {EventSource} The event source object to allow for cancellation.
 */
export const streamSearch = (queryText, { onProgress, onResults, onError }) => {
  // Use a GET request with a query parameter for EventSource
  const url = `${API_URL}/search/stream?q=${encodeURIComponent(queryText)}`;
  const eventSource = new EventSource(url);

  // Listener for incoming messages
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);

    // Handle progress updates
    if (data.progress < 100) {
      onProgress(data);
    }
    
    // Handle the final message with results
    if (data.results) {
      onResults(data.results);
      eventSource.close(); // We're done, close the connection
    }

    // Handle any error sent from the backend stream
    if (data.error) {
        onError(data.error);
        eventSource.close();
    }
  };

  // Listener for connection errors
  eventSource.onerror = (err) => {
    console.error("EventSource failed:", err);
    onError('Failed to connect to the search server. Please try again.');
    eventSource.close();
  };

  return eventSource; // Return it so the component can close it if needed
};