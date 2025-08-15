import torch
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class CLIPService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CLIPService, cls).__new__(cls)
            # Initialize the model on first instantiation
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"Loading CLIP model '{settings.CLIP_MODEL_NAME}' onto device '{device}'...")
            cls._model = SentenceTransformer(settings.CLIP_MODEL_NAME, device=device)
            print("CLIP model loaded successfully.")
        return cls._instance

    def get_model(self):
        return self._model

    def encode_text(self, text: str):
        """Generates an embedding for a given text query."""
        return self.get_model().encode(text, convert_to_tensor=True)

# Instantiate the singleton on module load
clip_service = CLIPService()

def get_clip_service():
    """Dependency injector for FastAPI."""
    return clip_service