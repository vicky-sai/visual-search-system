import chromadb
from app.core.config import settings

class ChromaDBService:
    _instance = None
    _client = None
    _collection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaDBService, cls).__new__(cls)
            print(f"Initializing ChromaDB client and connecting to collection '{settings.CHROMA_COLLECTION_NAME}'...")
            cls._client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
            cls._collection = cls._client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            print("ChromaDB service initialized successfully.")
        return cls._instance

    def get_collection(self):
        return self._collection

    # --- THIS IS THE FIX ---
    # We add `include` as a parameter to our custom search function
    def search(self, query_embedding, top_k=5, include=["metadatas"]):
        """Performs a similarity search in the collection."""
        return self.get_collection().query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            include=include # And then we use that parameter here
        )
    # ---------------------

# Instantiate the singleton on module load
chromadb_service = ChromaDBService()

def get_chromadb_service():
    """Dependency injector for FastAPI."""
    return chromadb_service