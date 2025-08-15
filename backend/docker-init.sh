#!/bin/sh

# This is the ONE AND ONLY master initialization script.
# It waits for Ollama, pulls the model, and runs data processing.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- 1. Wait for the Ollama Server to be Ready ---
echo "--- Initializing: Waiting for Ollama API server..."
until curl -sSf http://ollama:11434/api/tags > /dev/null; do
    printf "."
    sleep 1
done
echo "\nOllama API is up and running!"


# --- 2. Pull the Required Ollama Model ---
echo "--- Checking for AI model: $OLLAMA_MODEL ---"
MODEL_EXISTS=$(curl -s http://ollama:11434/api/tags | jq --arg model "$OLLAMA_MODEL" '.models | map(.name == $model) | any')

if [ "$MODEL_EXISTS" = "true" ]; then
    echo "Model '$OLLAMA_MODEL' already exists. Skipping download."
else
    echo "Model '$OLLAMA_MODEL' not found. Starting download..."
    curl -sN -X POST http://ollama:11434/api/pull \
      -H "Content-Type: application/json" \
      -d "{\"name\":\"$OLLAMA_MODEL\"}" \
    | jq -r --unbuffered 'select(.status=="downloading") | "Downloading model: " + (.completed / .total * 100 | floor | tostring) + "%"'
    echo "\nModel pull complete for: $OLLAMA_MODEL"
fi


# --- 3. Run the Python Data Processing Scripts ---
echo "--- Running data preparation scripts ---"
export PYTHONPATH=.
echo "Step 3a: Downloading images..."
python scripts/download_images.py
echo "Step 3b: Generating embeddings..."
python scripts/generate_embeddings.py


echo "--- VICKY VISUAL SEARCH INITIALIZATION COMPLETE ---"