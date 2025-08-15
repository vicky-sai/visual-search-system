import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- App Configuration ---
    APP_NAME: str = "Visual Search API"
    API_V1_STR: str = "/api/v1"

    # --- Data and Script Configuration (NEW) ---
    DATA_DIR: str = "data"
    IMAGES_DIR: str = os.path.join(DATA_DIR, "images")
    CSV_PATH: str = os.path.join(DATA_DIR, "photos_url.csv")
    NUM_IMAGES_TO_DOWNLOAD: int | None = 500 # Set to None to download all
    IMAGE_TARGET_SIZE: tuple = (800, 800)

    # --- Model & Embedding Configuration ---
    CLIP_MODEL_NAME: str = 'clip-ViT-B-32'
    
    # --- ChromaDB Configuration ---
    CHROMA_PERSIST_DIR: str = "storage/chromadb"
    CHROMA_COLLECTION_NAME: str = "visual_search"

    # --- Ollama Configuration ---
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gemma3:4b"
    EXPLANATION_PROMPT: str = (
        "You are an AI assistant for a visual search engine. "
        "The user searched for: '{query}'. A relevant image was found. "
        "Generate a single, concise, and business-friendly sentence explaining why an image could be relevant to this search. "
        "Focus on the key objects, actions, or concepts in the user's query. Do not mention the image itself. "
        "Example: 'This result may be relevant as it features a dog playing fetch on a sunny beach.'"
    )
    
    # --- CORS Configuration ---
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

# Instantiate the settings
settings = Settings()