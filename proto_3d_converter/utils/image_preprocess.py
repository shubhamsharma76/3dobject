"""
Image preprocessing module for the 3D converter.
Handles loading, background removal, and other preprocessing steps.
"""

import os
import cv2
import numpy as np
from rembg import remove
from PIL import Image

def preprocess_image(image_path, output_dir='outputs'):
    """
    Preprocess an image by removing background and preparing it for 3D conversion
    
    Args:
        image_path (str): Path to the input image
        output_dir (str): Directory to save processed outputs
        
    Returns:
        str: Path to the processed image
    """
    # Check if image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load image
    input_img = cv2.imread(image_path)
    if input_img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    # Convert to RGB for processing
    input_img_rgb = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
    
    # Remove background
    print("Removing background...")
    input_pil = Image.fromarray(input_img_rgb)
    output_pil = remove(input_pil)
    
    # Convert back to numpy array
    output_array = np.array(output_pil)
    
    # Save the background-removed image
    output_path = os.path.join(output_dir, 'removed_bg.png')
    cv2.imwrite(output_path, cv2.cvtColor(output_array, cv2.COLOR_RGBA2BGRA))
    
    print(f"Saved background-removed image at {output_path}")
    return output_path