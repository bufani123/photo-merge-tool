# Image Merger Tool

A Python tool for merging two images into a 4:3 vertical format. Supports random combinations and manual merging with adjustable image offsets.

## Features

- Merges two images into a 4:3 vertical format.
- Allows random selection of image pairs from a folder.
- Supports custom offset for the first image in the merged result.
- Avoids overwriting existing files by generating unique output filenames.

## Requirements

- Python 3.x
- PIL (Python Imaging Library) or Pillow

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/image-merger.git
   cd image-merger
   
2. Install dependencies:
   pip install pillow

## Usage
Command-line Interface
To generate random combinations of images:

python photo-merge-tool.py /path/to/your/images --num_images 5 --offset 50 --output_folder /path/to/output
This will generate 5 merged images, each with the first image having a vertical offset of 50 pixels and saving them to the specified output folder.

To merge specific images:
python photo-merge-tool.py /path/to/your/images --image1 "image1.jpg" --image2 "image2.jpg" --output "merged.jpg" --offset 50 --output_folder /path/to/output

Arguments
folder_path: Path to the folder containing images.
--num_images: Number of image pairs to combine randomly (default is 5).
--offset: Vertical offset for the first image in the merged result (default is 0).
--output_folder: Folder where the merged images will be saved. If not provided, the images are saved in the current working directory.
--image1, --image2: Names of the specific images to merge.
--output: Output filename for specific image merge (default is combined_specific.jpg).

## Usage
Copyright (c) [2025] [AIyj-cmd]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
