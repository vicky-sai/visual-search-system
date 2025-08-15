import ollama
from app.core.config import settings

class ExplanationService:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExplanationService, cls).__new__(cls)
            print(f"Initializing Ollama client with base URL: {settings.OLLAMA_BASE_URL}")
            cls._client = ollama.Client(host=settings.OLLAMA_BASE_URL)
        return cls._instance

    def get_client(self):
        return self._client

    def generate_explanation(self, user_query: str) -> str:
        """Generates an explanation for a search query using the Ollama model."""
        try:
            prompt = settings.EXPLANATION_PROMPT.format(query=user_query)
            
            response = self.get_client().generate(
                model=settings.OLLAMA_MODEL,
                prompt=prompt
            )
            return response['response'].strip()
        except Exception as e:
            print(f"Error calling Ollama API: {e}")
            return "An explanation could not be generated at this time."

# Instantiate the singleton
explanation_service = ExplanationService()

def get_explanation_service():
    """Dependency injector for FastAPI."""
    return explanation_service