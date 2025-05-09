# Proto3D Converter

A simple prototype that converts photos or text prompts to 3D models.

## Features

- Accepts either image input (jpg/png) or text prompts
- Automatically removes background from images
- Generates 3D models (.obj format) 
- Visualizes the resulting 3D model
- Simple command line interface

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/proto-3d-converter.git
cd proto-3d-converter
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Run the script with appropriate arguments:

```bash
# For image input
python main.py --input_type image --input path/to/your/image.jpg

# For text input
python main.py --input_type text --input "A small toy car"
```

### Interactive Mode

Run the script without arguments for interactive mode:

```bash
python main.py
```

Then follow the prompts to enter input type and either the image path or text prompt.

## Project Structure

```
proto-3d-converter/
├── main.py               # Main entry point
├── utils/                # Utility modules
│   ├── __init__.py
│   ├── image_preprocess.py  # Image preprocessing functions
│   ├── text_to_3d.py        # Text to 3D conversion
│   ├── image_to_3d.py       # Image to 3D conversion
│   └── visualization.py     # 3D model visualization
├── requirements.txt      # Required packages
└── README.md             # This file
```

## How It Works

### Image Input

1. The input image is loaded and background is removed using the `rembg` library
2. The cleaned image is processed to create a heightmap
3. The heightmap is used to generate a 3D mesh
4. The mesh is saved as an OBJ file and visualized

### Text Input

1. The text prompt is analyzed to extract keywords related to shapes and sizes
2. Based on the extracted keywords, an appropriate 3D primitive or composite shape is created
3. The resulting mesh is saved as an OBJ file and visualized

## Libraries Used

- OpenCV: Image processing
- rembg: Background removal
- trimesh: 3D mesh creation and manipulation
- matplotlib: 3D visualization
- scipy: Image filtering and processing
- numpy: Numerical operations
- PIL: Image manipulation

## Thought Process

This prototype demonstrates a minimalist approach to generating 3D models from either images or text prompts. 

For the image pathway, instead of using complex AI-based reconstruction methods which would require substantial resources, I opted for a heightmap-based approach that creates a 3D surface from a 2D image. This works best with images that have clear object boundaries and simple shapes.

For the text pathway, I implemented a keyword extraction system that can identify object types and size descriptors. This allows the system to generate appropriate primitive shapes or composite objects based on the description provided. While not as sophisticated as deep learning text-to-3D approaches, this method is lightweight and provides reasonable results for simple descriptions.

The modular design allows for easy extension in the future, such as integrating more sophisticated AI-based 3D generation techniques when they become more accessible.

## Limitations and Future Improvements

- The current image-to-3D conversion creates simplified convex hull representations and lacks detail
- The text-to-3D system is limited to a predefined set of objects and primitives
- Integration with more advanced AI models would improve the quality of generated models
- Adding texture support would make the 3D models more realistic