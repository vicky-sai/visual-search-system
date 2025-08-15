from pydantic import BaseModel
from typing import List

# --- API Request Models ---

class SearchQuery(BaseModel):
    text: str

# --- API Response Models ---

class SearchResultItem(BaseModel):
    image_id: str
    image_url: str
    explanation: str

class SearchResponse(BaseModel):
    results: List[SearchResultItem]