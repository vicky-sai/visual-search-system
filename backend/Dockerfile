# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install curl and jq
RUN apt-get update && apt-get install -y curl jq && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code
COPY . .

# --- THIS IS THE FIX ---
# We now only need to make our ONE master script executable.
RUN chmod +x /app/docker-init.sh
# The line for 'init_data.sh' has been removed.
# --------------------

# Expose the port the app runs on
EXPOSE 8000

# The default command for the main 'backend' service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]