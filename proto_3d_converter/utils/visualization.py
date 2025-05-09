"""
3D model visualization module.
Handles displaying 3D models using matplotlib or pyrender.
"""

import os
import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def visualize_3d_model(model_path, method='matplotlib'):
    """
    Visualize a 3D model using matplotlib or pyrender
    
    Args:
        model_path (str): Path to the 3D model file
        method (str): Visualization method ('matplotlib' or 'pyrender')
        
    Returns:
        None (displays the visualization)
    """
    # Load the mesh
    try:
        mesh = trimesh.load(model_path)
    except Exception as e:
        print(f"Error loading mesh: {e}")
        return
    
    if method == 'matplotlib':
        # Visualize using matplotlib
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Get mesh data
        vertices = mesh.vertices
        faces = mesh.faces
        
        # Plot the triangles
        tri = Axes3D.plot_trisurf(
            ax,
            vertices[:, 0], vertices[:, 1], vertices[:, 2],
            triangles=faces,
            cmap=cm.viridis,
            shade=True
        )
        
        # Set equal aspect ratio
        max_range = np.array([
            vertices[:, 0].max() - vertices[:, 0].min(),
            vertices[:, 1].max() - vertices[:, 1].min(),
            vertices[:, 2].max() - vertices[:, 2].min()
        ]).max() / 2.0
        
        mid_x = (vertices[:, 0].max() + vertices[:, 0].min()) * 0.5
        mid_y = (vertices[:, 1].max() + vertices[:, 1].min()) * 0.5
        mid_z = (vertices[:, 2].max() + vertices[:, 2].min()) * 0.5
        
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Model Visualization')
        
        plt.tight_layout()
        plt.show()
        
    elif method == 'pyrender':
        # Try to use pyrender if available
        try:
            import pyrender
            from pyrender import Mesh, Scene, Viewer
            
            # Create a scene and add the mesh
            scene = Scene()
            mesh_render = Mesh.from_trimesh(mesh)
            scene.add(mesh_render)
            
            # Create a viewer
            viewer = Viewer(scene, use_raymond_lighting=True)
            
        except ImportError:
            print("Pyrender not installed. Using matplotlib instead.")
            visualize_3d_model(model_path, method='matplotlib')
    else:
        print(f"Unsupported visualization method: {method}")