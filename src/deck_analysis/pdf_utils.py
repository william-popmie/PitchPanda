"""
Utilities for converting PDF pitch decks to images.
"""
import os
import base64
from typing import List
from pathlib import Path


def pdf_to_images(pdf_path: str, output_dir: str = None) -> List[str]:
    """
    Convert PDF pages to images.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save images (optional, defaults to temp)
    
    Returns:
        List of paths to generated image files
    """
    try:
        from pdf2image import convert_from_path
    except ImportError:
        raise ImportError(
            "pdf2image is required for PDF conversion. "
            "Install with: pip install pdf2image\n"
            "Also requires poppler-utils: brew install poppler (macOS)"
        )
    
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(pdf_path), "temp_images")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=150)
    
    image_paths = []
    deck_name = Path(pdf_path).stem
    
    for i, image in enumerate(images, start=1):
        img_path = os.path.join(output_dir, f"{deck_name}_slide_{i:03d}.png")
        image.save(img_path, "PNG")
        image_paths.append(img_path)
    
    return image_paths


def encode_image_base64(image_path: str) -> str:
    """
    Encode image to base64 for GPT-4 Vision API.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Base64 encoded string
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
