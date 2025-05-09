"""
Proto3D Converter: Convert images or text to 3D models
Main entry point for the application
"""

import os
import argparse
from utils.image_preprocess import preprocess_image
from utils.text_to_3d import generate_3d_from_text
from utils.image_to_3d import generate_3d_from_image
from utils.visualization import visualize_3d_model

# Ensure necessary directories exist
os.makedirs('outputs', exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Convert images or text to 3D models')
    parser.add_argument('--input_type', type=str, choices=['image', 'text'], 
                        help='Type of input (image/text)')
    parser.add_argument('--input', type=str, help='Path to image or text prompt')
    parser.add_argument('--output_dir', type=str, default='outputs', 
                        help='Directory to save outputs')
    
    args = parser.parse_args()
    
    # If args not provided, ask user interactively
    if not args.input_type:
        input_type = input("Input type (image/text): ").lower()
        while input_type not in ['image', 'text']:
            print("Invalid input type. Please enter 'image' or 'text'")
            input_type = input("Input type (image/text): ").lower()
        args.input_type = input_type
    
    if not args.input:
        args.input = input(f"Enter {'image path' if args.input_type == 'image' else 'text prompt'}: ")
    
    # Process based on input type
    if args.input_type == 'image':
        # Process image
        print(f"Image path: {args.input}")
        print("Loading and preprocessing image...")
        
        # Preprocess the image (background removal)
        processed_img_path = preprocess_image(args.input, args.output_dir)
        
        # Generate 3D model from processed image
        print("Generating 3D model from image...")
        model_path = generate_3d_from_image(processed_img_path, args.output_dir)
        
    else:
        # Process text prompt
        print(f"Text prompt: {args.input}")
        print("Generating 3D model from text...")
        
        # Generate 3D model from text
        model_path = generate_3d_from_text(args.input, args.output_dir)
    
    print(f"Saved 3D model at {model_path}")
    
    # Visualize the model
    print("Visualizing model...")
    visualize_3d_model(model_path)
    
    print("Done!")

if __name__ == "__main__":
    main()