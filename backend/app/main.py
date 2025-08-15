from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1 import search
from app.services import clip_service, chromadb_service, explanation_service

# Application an_instance
app = FastAPI(
    title=settings.APP_NAME,
    # Lifespan events are recommended over on_event for modern FastAPI
)

# --- Event Handlers ---
# This dictionary-based approach is for older FastAPI versions.
# For newer versions (0.93.0+), use lifespan context manager.
# This ensures models are loaded on startup.
@app.on_event("startup")
async def startup_event():
    print("--- Backend App Startup ---")
    # This will trigger the instantiation of our singleton services
    clip_service.get_clip_service()
    chromadb_service.get_chromadb_service()
    explanation_service.get_explanation_service()
    print("--- All services initialized ---")

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static Files ---
# Mount the 'data/images' directory to be served at '/images'
app.mount("/images", StaticFiles(directory="data/images"), name="images")

# --- API Routers ---
app.include_router(search.router, prefix=settings.API_V1_STR)

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to the {settings.APP_NAME}"}