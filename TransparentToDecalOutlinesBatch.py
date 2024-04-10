import os
from PIL import Image, ImageFilter, ImageOps

def add_outline_to_transparent_image(input_folder, output_folder, border_size=20, border_color=(255, 255, 255), expand_size=100, antialias=2):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Ensure the border size is odd for the filter
    if border_size % 2 == 0:
        border_size += 1
    
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if not filename.endswith(('.png', '.jpg', '.jpeg')):
            continue  # Skip non-image files
        
        # Construct the full file path
        input_path = os.path.join(input_folder, filename)
        
        # Load the image
        image = Image.open(input_path)
        
        # Ensure the image has an alpha channel
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Expand the image canvas by 100 units each side with transparent padding
        expanded_image = ImageOps.expand(image, border=expand_size, fill=(0,0,0,0))
        
        # Extract the alpha channel and apply a dilation filter, which expands the area of the non-transparent parts
        alpha = expanded_image.getchannel('A')
        mask = alpha.point(lambda p: 255 if p > 0 else 0)
        
        # Apply the dilation filter to the mask
        mask = mask.filter(ImageFilter.MaxFilter(border_size))

        # Apply a smaller blur for anti-aliasing
        mask = mask.filter(ImageFilter.GaussianBlur(antialias))

        # Expand the mask to compensate for the blur and to make the border sharper
        mask = ImageOps.expand(mask, border=1)

        # Create a new image for the border, filled with the border color but transparent
        border = Image.new('RGBA', expanded_image.size, border_color + (0,))
        border.paste(border_color + (255,), mask=mask)
        
        # Composite the expanded image onto the border to apply the border around the character
        final_image_with_border = Image.alpha_composite(border, expanded_image)
        
        # Save the modified image to the output folder
        output_path = os.path.join(output_folder, filename)
        final_image_with_border.save(output_path)

# Example usage:
input_folder = ""
output_folder = ""
add_outline_to_transparent_image(input_folder, output_folder, border_size=20, expand_size=100, antialias=1)  # Reduced antialias for sharper edges