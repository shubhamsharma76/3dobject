"""
Image to 3D conversion module.
Converts preprocessed images to 3D models.
"""

import os
import cv2
import numpy as np
import trimesh
from scipy.ndimage import gaussian_filter

def generate_3d_from_image(image_path, output_dir='outputs'):
    """
    Generate a 3D model from a preprocessed image (with background removed)
    
    Args:
        image_path (str): Path to preprocessed image
        output_dir (str): Directory to save the 3D model
    
    Returns:
        str: Path to the saved 3D model
    """
    # Load the image with alpha channel
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    # Check if image has alpha channel, if not add one
    if img.shape[2] == 3:
        alpha = np.ones((img.shape[0], img.shape[1], 1), dtype=img.dtype) * 255
        img = np.concatenate((img, alpha), axis=2)
    
    # Convert to grayscale for heightmap
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    
    # Apply Gaussian filter for smoothing
    gray_smooth = gaussian_filter(gray, sigma=1.0)
    
    # Normalize the heightmap
    height_map = gray_smooth / 255.0
    
    # Create vertices and faces for the mesh
    rows, cols = height_map.shape
    vertices = []
    faces = []
    
    # Create vertices (x, y, z)
    scale_factor = 0.1  # Scale the z-axis for better visualization
    for y in range(rows):
        for x in range(cols):
            # Skip vertices with zero alpha (background)
            if img[y, x, 3] > 0:
                z = height_map[y, x] * scale_factor
                vertices.append([x / cols - 0.5, (rows - y) / rows - 0.5, z])
    
    # Convert to numpy array
    vertices = np.array(vertices)
    
    # If we don't have enough vertices, generate a simple primitive
    if len(vertices) < 100:
        print("Not enough valid vertices found, creating a simple primitive instead")
        # Create a simple cube
        mesh = trimesh.creation.box(extents=[0.5, 0.5, 0.5])
    else:
        # Create a point cloud with the vertices
        cloud = trimesh.points.PointCloud(vertices)
        
        # Create a convex hull from the point cloud
        try:
            mesh = trimesh.convex.convex_hull(cloud.vertices)
        except (ValueError, IndexError):
            print("Failed to create convex hull, creating a simple primitive instead")
            mesh = trimesh.creation.box(extents=[0.5, 0.5, 0.5])
    
    # Save the mesh as an OBJ file
    model_path = os.path.join(output_dir, 'model.obj')
    mesh.export(model_path)
    
    return model_path