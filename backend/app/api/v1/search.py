import asyncio
import json
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, Request

from app.core.models import SearchQuery, SearchResponse, SearchResultItem
from app.services.clip_service import get_clip_service, CLIPService
from app.services.chromadb_service import get_chromadb_service, ChromaDBService
from app.services.explanation_service import get_explanation_service, ExplanationService

router = APIRouter()

def format_sse(data: dict) -> str:
    """Formats a dictionary as a Server-Sent Event string."""
    return f"data: {json.dumps(data)}\n\n"

# @router.get("/search/stream")
# async def stream_search_images(
#     q: str,
#     request: Request,
#     clip: CLIPService = Depends(get_clip_service),
#     chroma: ChromaDBService = Depends(get_chromadb_service),
#     explainer: ExplanationService = Depends(get_explanation_service)
# ):
#     # --- THIS IS THE FIX ---
#     # The nested generator needs access to the variables from the parent function.
#     # We pass them in as arguments.
#     async def event_generator(query: str, clip_service: CLIPService, chroma_service: ChromaDBService, explainer_service: ExplanationService):
#         try:
#             # Step 1: Text Embedding
#             yield format_sse({"step": "Analyzing your query...", "progress": 25})
#             query_embedding = clip_service.encode_text(query) # Use the passed-in argument
#             await asyncio.sleep(0.001)

#             # Step 2: Vector Search
#             yield format_sse({"step": "Searching our visual library...", "progress": 50})
#             search_results = chroma_service.search( # Use the passed-in argument
#                 query_embedding=query_embedding, 
#                 top_k=5, 
#                 include=["metadatas", "distances"]
#             )
#             await asyncio.sleep(0.01)

#             # Step 3: AI Explanation
#             yield format_sse({"step": "Asking our AI for an explanation...", "progress": 75})
#             explanation_text = explainer_service.generate_explanation(user_query=query) # Use the passed-in argument
#             await asyncio.sleep(0.001)

#             # Step 4: Formatting Response
#             yield format_sse({"step": "Finalizing results...", "progress": 95})
#             response_items = []
#             if search_results and search_results['ids'][0]:
#                 for i, result_id in enumerate(search_results['ids'][0]):
#                     filename = search_results['metadatas'][0][i]['filename']
#                     distance = search_results['distances'][0][i]
#                     similarity = max(0, 1 - distance / 2)
#                     similarity_percent = round(similarity * 100)
                    
#                     image_url = f"{request.base_url}images/{filename}"
#                     response_items.append({
#                         "image_id": result_id,
#                         "image_url": image_url,
#                         "explanation": explanation_text,
#                         "score": similarity_percent
#                     })
            
#             # Final Step
#             final_data = {
#                 "step": "Done!", 
#                 "progress": 100, 
#                 "results": response_items
#             }
#             yield format_sse(final_data)

#         except Exception as e:
#             print(f"Error during stream: {e}")
#             error_data = {"error": "An error occurred during the search.", "progress": 100}
#             yield format_sse(error_data)

#     # We call the generator with the necessary arguments.
#     return StreamingResponse(event_generator(q, clip, chroma, explainer), media_type="text/event-stream")


@router.get("/search/stream")
async def stream_search_images(
    q: str,
    request: Request,
    clip: CLIPService = Depends(get_clip_service),
    chroma: ChromaDBService = Depends(get_chromadb_service),
    explainer: ExplanationService = Depends(get_explanation_service)
):
    async def event_generator():
        loop = asyncio.get_running_loop()

        try:
            # Step 1: Embed text
            yield format_sse({"step": "Analyzing your query...", "progress": 25})
            query_embedding = await loop.run_in_executor(None, clip.encode_text, q)

            # Step 2: Vector DB search
            yield format_sse({"step": "Searching our visual library...", "progress": 50})
            search_results = await loop.run_in_executor(
                None,
                chroma.search,
                query_embedding, 5, ["metadatas", "distances"]
            )

            # Step 3: Explanation
            yield format_sse({"step": "Asking our AI for an explanation...", "progress": 75})
            explanation_text = await loop.run_in_executor(
                None, explainer.generate_explanation, q
            )

            # Step 4: Package response
            yield format_sse({"step": "Finalizing results...", "progress": 95})
            response_items = []
            if search_results and search_results['ids'][0]:
                for i, result_id in enumerate(search_results['ids'][0]):
                    meta = search_results['metadatas'][0][i]
                    distance = search_results['distances'][0][i]
                    similarity = max(0, 1 - distance / 2)
                    similarity_percent = round(similarity * 100)
                    response_items.append({
                        "image_id": result_id,
                        "image_url": f"{request.base_url}images/{meta['filename']}",
                        "explanation": explanation_text,
                        "score": similarity_percent
                    })

            yield format_sse({
                "step": "Done!",
                "progress": 100,
                "results": response_items
            })

        except Exception as e:
            print(f"Stream Exception: {e}")
            yield format_sse({
                "error": "An error occurred during the search.",
                "progress": 100
            })

    return StreamingResponse(event_generator(), media_type="text/event-stream")
