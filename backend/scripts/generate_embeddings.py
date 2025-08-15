"""
Image Embedding Generation and Indexing
---------------------------------------
This script generates vector embeddings for images using a pre-trained CLIP model
and stores them in a persistent ChromaDB collection.

Requirements:
    pip install chromadb sentence-transformers torch pillow tqdm

Usage:
    1. First, run 'download_images.py' to ensure images are in 'data/images'.
    2. Run this script from the 'backend' folder: python scripts/generate_embeddings.py
    3. Embeddings will be stored in the 'storage/chromadb' directory.
"""
import os
import torch
from PIL import Image
from sentence_transformers import SentenceTransformer
import chromadb
from tqdm import tqdm

# --- Configuration ---
# Set up paths relative to the 'backend' directory
IMG_DIR = os.path.join("data", "images")
CHROMA_PERSIST_DIR = os.path.join("storage", "chromadb")
CHROMA_COLLECTION_NAME = "visual_search"

# Model and device configuration
MODEL_NAME = 'clip-ViT-B-32'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
BATCH_SIZE = 64 # Adjust based on your VRAM/RAM

def setup_chromadb_client():
    """Initializes and returns a persistent ChromaDB client."""
    print(f"Initializing ChromaDB client at: {CHROMA_PERSIST_DIR}")
    return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

def get_image_files(directory):
    """Returns a sorted list of all JPG image files in the directory."""
    return sorted([f for f in os.listdir(directory) if f.lower().endswith('.jpg')])

def get_already_processed_ids(collection):
    """Fetches the IDs of all items already in the Chroma collection."""
    print("Checking for already processed images in ChromaDB...")
    existing_items = collection.get(include=[]) # Fetches all items without embeddings/metadatas
    return set(existing_items['ids'])

def process_batch(batch_files, model, collection):
    """Processes a batch of images, generates embeddings, and adds them to ChromaDB."""
    image_paths = [os.path.join(IMG_DIR, f) for f in batch_files]
    
    try:
        # Open images and generate embeddings
        images = [Image.open(p) for p in image_paths]
        embeddings = model.encode(images, batch_size=len(images), convert_to_tensor=True, show_progress_bar=False, device=DEVICE)
        
        # Prepare data for ChromaDB
        ids = [os.path.splitext(f)[0] for f in batch_files]
        metadatas = [{'filename': f} for f in batch_files]
        
        # Add to collection
        collection.add(
            embeddings=embeddings.cpu().tolist(), # Add embeddings as lists
            metadatas=metadatas,
            ids=ids
        )
    except Exception as e:
        print(f"\nError processing batch starting with {batch_files[0]}: {e}")
        print("Skipping this batch.")

def main():
    """Main function to orchestrate the embedding generation process."""
    print("--- Starting Embedding Generation and Indexing ---")
    
    if not os.path.exists(IMG_DIR):
        print(f"Error: Image directory not found at '{IMG_DIR}'.")
        print("Please run the 'download_images.py' script first.")
        return

    # --- 1. Initialize Model and DB ---
    print(f"Loading CLIP model '{MODEL_NAME}' on device '{DEVICE}'...")
    model = SentenceTransformer(MODEL_NAME, device=DEVICE)

    client = setup_chromadb_client()
    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"} # Using cosine similarity for search
    )
    
    # --- 2. Identify Images to Process ---
    all_image_files = get_image_files(IMG_DIR)
    processed_ids = get_already_processed_ids(collection)
    
    files_to_process = [
        f for f in all_image_files if os.path.splitext(f)[0] not in processed_ids
    ]
    
    if not files_to_process:
        print("All images are already processed and indexed. Nothing to do.")
        return
        
    print(f"Found {len(all_image_files)} total images.")
    print(f"Found {len(processed_ids)} already processed images.")
    print(f"Processing {len(files_to_process)} new images...")

    # --- 3. Process Images in Batches ---
    with tqdm(total=len(files_to_process), desc="Generating Embeddings") as pbar:
        for i in range(0, len(files_to_process), BATCH_SIZE):
            batch_files = files_to_process[i:i + BATCH_SIZE]
            process_batch(batch_files, model, collection)
            pbar.update(len(batch_files))

    print("\n--- Embedding Generation and Indexing Complete ---")
    print(f"Total items in collection '{CHROMA_COLLECTION_NAME}': {collection.count()}")

if __name__ == "__main__":
    main()