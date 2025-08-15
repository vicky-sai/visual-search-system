# Vicky Visual Search

... (description) ...

## Prerequisites

-   [Docker](https://www.docker.com/products/docker-desktop/) installed and running.

## Quickstart: How to Run the Project

The entire application, including data initialization, is managed by Docker Compose.

### Step 1: Build and Start All Services

This single command will:
1.  Build the application images.
2.  Start the Ollama model server.
3.  **Automatically run a one-time job to download images and generate embeddings.**
4.  Start the backend and frontend servers once the data is ready.

```bash
docker-compose up --build -d
```
*The `-d` flag runs the containers in detached mode.*

**Note:** The very first time you run this, the `init-backend` service will take several minutes to download images and create the database. You can view its progress by running: `docker-compose logs -f init-backend`. Once it shows "DATA INITIALIZATION COMPLETE", it's done. This only runs once; on subsequent startups, it will see the data already exists and finish quickly.

### Step 2: Download the AI Model (First-Time Setup)

The Ollama container starts empty. Tell it to download the `gemma:2b` model.

```bash
docker-compose exec ollama ollama run gemma:2b
```
*(You only need to do this once.)*

### Step 3: Use the Application!

The entire system is now running and fully initialized.

-   **Frontend UI**: Open your browser to [**http://localhost:5173**](http://localhost:5173)
-   **Backend API Docs**: The API is available at [**http://localhost:8000**](http://localhost:8000)

## To Stop the Application
```bash
docker-compose down
```