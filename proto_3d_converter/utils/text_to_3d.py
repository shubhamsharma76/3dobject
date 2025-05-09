"""
Text to 3D conversion module.
Converts text prompts to 3D models.
"""

import os
import re
import numpy as np
import trimesh
import random

def generate_3d_from_text(text_prompt, output_dir='outputs'):
    """
    Generate a 3D model from a text prompt
    
    Args:
        text_prompt (str): Text prompt describing the desired object
        output_dir (str): Directory to save the 3D model
        
    Returns:
        str: Path to the saved 3D model
    """
    # Extract keywords from text prompt
    keywords = extract_keywords(text_prompt.lower())
    
    # Generate a mesh based on keywords
    mesh = create_shape_from_keywords(keywords)
    
    # Save the mesh as an OBJ file
    model_path = os.path.join(output_dir, 'model.obj')
    mesh.export(model_path)
    
    return model_path

def extract_keywords(text):
    """Extract relevant shape keywords from the text prompt"""
    shape_keywords = {
        'sphere': ['sphere', 'ball', 'round', 'circular'],
        'cube': ['cube', 'box', 'square', 'rectangular', 'block'],
        'cylinder': ['cylinder', 'cylindrical', 'tube', 'pipe'],
        'cone': ['cone', 'conical', 'pyramid'],
        'torus': ['torus', 'donut', 'ring', 'circular tube'],
        'car': ['car', 'vehicle', 'automobile'],
        'chair': ['chair', 'seat', 'stool'],
        'table': ['table', 'desk'],
        'mug': ['mug', 'cup', 'glass'],
        'bottle': ['bottle', 'flask']
    }
    
    # Find matches for each shape keyword
    matches = {}
    for shape, keywords in shape_keywords.items():
        for keyword in keywords:
            if keyword in text:
                matches[shape] = matches.get(shape, 0) + 1
    
    # Get size cues from text
    size_multiplier = 1.0
    if any(word in text for word in ['small', 'tiny', 'little']):
        size_multiplier = 0.5
    elif any(word in text for word in ['large', 'big', 'huge', 'giant']):
        size_multiplier = 2.0
    
    # If no shape is matched, default to a random shape
    if not matches:
        shape = random.choice(list(shape_keywords.keys()))
    else:
        # Get the shape with the most matches
        shape = max(matches, key=matches.get)
    
    return {'shape': shape, 'size': size_multiplier}

def create_shape_from_keywords(keywords):
    """Create a 3D mesh based on the extracted keywords"""
    shape = keywords['shape']
    size = keywords['size']
    
    # Create the appropriate shape based on keywords
    if shape == 'sphere':
        mesh = trimesh.creation.icosphere(radius=0.5 * size)
    elif shape == 'cube':
        mesh = trimesh.creation.box(extents=[size, size, size])
    elif shape == 'cylinder':
        mesh = trimesh.creation.cylinder(radius=0.3 * size, height=size)
    elif shape == 'cone':
        mesh = trimesh.creation.cone(radius=0.5 * size, height=size)
    elif shape == 'torus':
        # Fix for the missing arguments error
        mesh = trimesh.creation.torus(
            radius=0.5 * size,  # major radius
            tube_radius=0.2 * size,  # minor radius
            major_segments=48,
            minor_segments=24
        )
    elif shape == 'car':
        # Create a simplified car shape
        body = trimesh.creation.box(extents=[size, 0.4 * size, 0.3 * size])
        top = trimesh.creation.box(extents=[0.6 * size, 0.3 * size, 0.2 * size])
        top.apply_translation([0, 0, 0.25 * size])
        wheel1 = trimesh.creation.cylinder(radius=0.1 * size, height=0.05 * size)
        wheel1.apply_translation([0.25 * size, 0.25 * size, -0.15 * size])
        wheel2 = trimesh.creation.cylinder(radius=0.1 * size, height=0.05 * size)
        wheel2.apply_translation([-0.25 * size, 0.25 * size, -0.15 * size])
        wheel3 = trimesh.creation.cylinder(radius=0.1 * size, height=0.05 * size)
        wheel3.apply_translation([0.25 * size, -0.25 * size, -0.15 * size])
        wheel4 = trimesh.creation.cylinder(radius=0.1 * size, height=0.05 * size)
        wheel4.apply_translation([-0.25 * size, -0.25 * size, -0.15 * size])
        mesh = trimesh.util.concatenate([body, top, wheel1, wheel2, wheel3, wheel4])
    elif shape == 'chair':
        # Create a simplified chair shape
        seat = trimesh.creation.box(extents=[size * 0.6, size * 0.6, size * 0.1])
        seat.apply_translation([0, 0, size * 0.4])
        back = trimesh.creation.box(extents=[size * 0.6, size * 0.1, size * 0.6])
        back.apply_translation([0, -size * 0.25, size * 0.7])
        leg1 = trimesh.creation.cylinder(radius=size * 0.05, height=size * 0.4)
        leg1.apply_translation([size * 0.25, size * 0.25, size * 0.2])
        leg2 = trimesh.creation.cylinder(radius=size * 0.05, height=size * 0.4)
        leg2.apply_translation([-size * 0.25, size * 0.25, size * 0.2])
        leg3 = trimesh.creation.cylinder(radius=size * 0.05, height=size * 0.4)
        leg3.apply_translation([size * 0.25, -size * 0.25, size * 0.2])
        leg4 = trimesh.creation.cylinder(radius=size * 0.05, height=size * 0.4)
        leg4.apply_translation([-size * 0.25, -size * 0.25, size * 0.2])
        mesh = trimesh.util.concatenate([seat, back, leg1, leg2, leg3, leg4])
    elif shape == 'table':
        # Create a simplified table shape
        top = trimesh.creation.box(extents=[size, size, size * 0.1])
        top.apply_translation([0, 0, size * 0.5])
        leg1 = trimesh.creation.cylinder(radius=size * 0.05, height=size * 0.5)
        leg1.apply_translation([size * 0.4, size * 0.4, size * 0.25])
        leg2 = trimesh.creation.cylinder(radius=size * 0.05, height=size * 0.5)
        leg2.apply_translation([-size * 0.4, size * 0.4, size * 0.25])
        leg3 = trimesh.creation.cylinder(radius=size * 0.05, height=size * 0.5)
        leg3.apply_translation([size * 0.4, -size * 0.4, size * 0.25])
        leg4 = trimesh.creation.cylinder(radius=size * 0.05, height=size * 0.5)
        leg4.apply_translation([-size * 0.4, -size * 0.4, size * 0.25])
        mesh = trimesh.util.concatenate([top, leg1, leg2, leg3, leg4])
    elif shape == 'mug':
        # Create a simplified mug shape
        body = trimesh.creation.cylinder(radius=0.3 * size, height=0.5 * size)
        inner = trimesh.creation.cylinder(radius=0.25 * size, height=0.45 * size)
        inner.apply_translation([0, 0, 0.025 * size])
        handle = trimesh.creation.annulus(r_min=0.05 * size, r_max=0, height=0.2 * size)
        handle.apply_translation([0.3 * size, 0, 0.2 * size])
        mesh = trimesh.boolean.difference([body, inner])
        mesh = trimesh.util.concatenate([mesh, handle])
    elif shape == 'bottle':
        # Create a simplified bottle shape
        body = trimesh.creation.cylinder(radius=0.2 * size, height=0.6 * size)
        neck = trimesh.creation.cylinder(radius=0.1 * size, height=0.2 * size)
        neck.apply_translation([0, 0, 0.4 * size])
        cap = trimesh.creation.cylinder(radius=0.12 * size, height=0.05 * size)
        cap.apply_translation([0, 0, 0.525 * size])
        mesh = trimesh.util.concatenate([body, neck, cap])
    else:
        # Default to a sphere
        mesh = trimesh.creation.icosphere(radius=0.5 * size)
    
    return mesh