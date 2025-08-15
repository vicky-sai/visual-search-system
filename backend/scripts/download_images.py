"""
Image Downloader for Photo Dataset
--------------------------------
This script downloads and optimizes images based on settings in app.core.config.
It must be run from the root 'backend' directory with the PYTHONPATH set.
Example: PYTHONPATH=. python scripts/download_images.py
"""
import os
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm

# --- Import the centralized settings ---
from app.core.config import settings

def download_images(csv_path, num_images, output_dir, target_size):
    """
    Download and optimize images from the provided CSV file.
    
    Args:
        csv_path (str): Path to the CSV file with photo URLs.
        num_images (int or None): Number of images to download.
        output_dir (str): Directory where images will be saved.
        target_size (tuple): The target (max) size for the images.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    # Read CSV and prepare dataset
    df = pd.read_csv(csv_path)
    if num_images:
        df = df.head(num_images)
    
    print(f"Downloading {len(df)} images to '{output_dir}'...")
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Downloading"):
        try:
            # Using row.name ensures we use the original CSV index, which is more robust
            image_index = row.name
            filename = f"{image_index:05d}.jpg" # e.g., 00000.jpg, 00001.jpg
            output_path = os.path.join(output_dir, filename)

            if os.path.exists(output_path):
                continue
            
            response = requests.get(row['photo_image_url'], timeout=10)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content))
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            img.save(output_path, 'JPEG', quality=85, optimize=True)
                
        except Exception as e:
            print(f"Error downloading image at index {idx} (URL: {row['photo_image_url']}): {e}")
            continue

if __name__ == "__main__":
    print("--- Starting Image Download Script ---")
    # --- The script now consumes settings from the config file ---
    download_images(
        csv_path=settings.CSV_PATH,
        num_images=settings.NUM_IMAGES_TO_DOWNLOAD,
        output_dir=settings.IMAGES_DIR,
        target_size=settings.IMAGE_TARGET_SIZE
    )
    print("--- Image Download Complete ---")