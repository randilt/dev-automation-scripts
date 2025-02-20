# This script iterates through all folders in the directory and move the files based on the suffix in the file name.
# It was used for a content migration task that required organizing images into 'tall' and 'square' folders.

import os
import shutil
from pathlib import Path

def organize_images(main_directory):
    # Convert to Path object for easier handling
    main_dir = Path(main_directory)
    
    # Common image extensions
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.JPG'}
    
    # Walk through all directories
    for directory in main_dir.rglob('*'):
        if not directory.is_dir():
            continue
            
        # Skip 'tall' and 'square' folders we create
        if directory.name in {'tall', 'square'}:
            continue
            
        # Find all image files in current directory
        image_files = []
        for ext in image_extensions:
            image_files.extend(directory.glob(f'*{ext}'))
        
        # If no images found, skip to next directory
        if not image_files:
            continue
            
        # Create tall and square subdirectories
        tall_dir = directory / 'tall'
        square_dir = directory / 'square'
        
        tall_dir.mkdir(exist_ok=True)
        square_dir.mkdir(exist_ok=True)
        
        # Process each image file
        for image_path in image_files:
            # Get the file name without extension
            name_without_ext = image_path.stem
            extension = image_path.suffix
            
            # Check if file has _tall or _square suffix
            if name_without_ext.endswith('_tall'):
                # Remove _tall suffix
                new_name = name_without_ext[:-5] + extension
                destination = tall_dir / new_name
                shutil.move(str(image_path), str(destination))
                
            elif name_without_ext.endswith('_square'):
                # Remove _square suffix
                new_name = name_without_ext[:-7] + extension
                destination = square_dir / new_name
                shutil.move(str(image_path), str(destination))

def main():
    # Get directory path from user
    directory = input("Enter the main directory path: ")
    
    try:
        organize_images(directory)
        print("Image organization completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()