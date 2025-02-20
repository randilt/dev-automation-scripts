# This script iterates through all folders in the directory and crops images based on predefined dimensions.  
# It was used for a content migration task that required cropping over 200 images into two different sizes.  
# The script utilizes the Pillow library for image processing, so ensure it is installed using:  
# pip install Pillow  

import os
from PIL import Image

def get_resampling_filter():
    """
    Get the appropriate resampling filter based on PIL version
    """
    if hasattr(Image, 'Resampling'):
        return Image.Resampling.LANCZOS
    return Image.LANCZOS

def crop_image(image, target_ratio, target_size):
    """
    Crop an image to specified aspect ratio and size from the center
    
    Parameters:
    image: PIL Image object
    target_ratio: tuple of (width, height) ratio
    target_size: tuple of (width, height) in pixels
    """
    # Get current dimensions
    width, height = image.size
    current_ratio = width / height
    target_ratio = target_ratio[0] / target_ratio[1]
    
    # Calculate crop box
    if current_ratio > target_ratio:  # Image is too wide
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = height
    else:  # Image is too tall
        new_height = int(width / target_ratio)
        left = 0
        top = (height - new_height) // 2
        right = width
        bottom = top + new_height
    
    # Crop and resize
    cropped = image.crop((left, top, right, bottom))
    return cropped.resize(target_size, get_resampling_filter())

def process_directory(input_dir):
    """
    Process all images in a directory and its subdirectories
    """
    # Define crop configurations
    crop_configs = [
        {
            'name': 'tall',
            'ratio': (9, 16),
            'size': (1080, 1920)
        },
        {
            'name': 'square',
            'ratio': (1, 1),
            'size': (700, 700)
        }
    ]
    
    # Supported image formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    
    # Walk through all subdirectories
    for root, _, files in os.walk(input_dir):
        print(f"Processing directory: {root}")
        
        # Process each file in the current directory
        for filename in files:
            # Check if file is an image
            if os.path.splitext(filename)[1].lower() in supported_formats:
                input_path = os.path.join(root, filename)
                name, ext = os.path.splitext(filename)
                
                try:
                    # Open image
                    with Image.open(input_path) as img:
                        # Convert to RGB if necessary
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        
                        # Flag to track successful processing
                        all_crops_successful = True
                        
                        # Process each crop configuration
                        for config in crop_configs:
                            try:
                                output_filename = f"{name}_{config['name']}{ext}"
                                output_path = os.path.join(root, output_filename)
                                
                                # Crop and save
                                cropped_img = crop_image(img, config['ratio'], config['size'])
                                
                                # Preserve quality settings based on format
                                if ext.lower() in ['.jpg', '.jpeg']:
                                    cropped_img.save(output_path, quality=95, subsampling=0)
                                else:
                                    cropped_img.save(output_path)
                            except Exception as e:
                                print(f"Error creating {config['name']} version of {filename}: {str(e)}")
                                all_crops_successful = False
                        
                        # Delete original file only if all crops were successful
                        if all_crops_successful:
                            os.remove(input_path)
                            print(f"Processed and deleted original: {filename}")
                        else:
                            print(f"Processed but kept original due to errors: {filename}")
                        
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

def main():
    # Get input directory from user
    input_dir = input("Enter the path to the main folder containing images: ").strip()
    
    # Verify directory exists
    if not os.path.isdir(input_dir):
        print("Error: Invalid directory path")
        return
    
    # Process all images
    print("Starting image processing...")
    process_directory(input_dir)
    print("Processing complete!")

if __name__ == "__main__":
    main()
