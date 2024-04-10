import os
from PIL import Image, ImageFilter


def place_decal_on_mockup(decal_folder, mockup_path, output_folder, decal_height, opacity=128, rotation_angle=-5):
    # Load the mockup image
    mockup = Image.open(mockup_path).convert("RGBA")

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all images in the decal folder
    for decal_filename in os.listdir(decal_folder):
        if not decal_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue  # Skip non-image files

        # Construct the full file path for the decal
        decal_path = os.path.join(decal_folder, decal_filename)

        # Load the decal
        decal = Image.open(decal_path).convert("RGBA")
        
        # Calculate new dimensions maintaining the aspect ratio
        aspect_ratio = decal.width / decal.height
        new_width = int(decal_height * aspect_ratio)

        # Resize the decal to the new height while maintaining aspect ratio
        decal = decal.resize((new_width, decal_height), Image.ANTIALIAS)

        # Adjust decal opacity
        alpha = decal.split()[3]
        alpha = alpha.point(lambda p: p * opacity // 255)
        decal.putalpha(alpha)

        #decal = decal.rotate(rotation_angle, expand=True, resample=Image.BICUBIC)
        #decal = decal.filter(ImageFilter.SMOOTH)

        # Calculate the position for the decal to be at the center of the mockup
        x = (mockup.width - decal.width) // 2
        y = (mockup.height - decal.height) // 2

        # Create a copy of the mockup to paste the decal onto
        result_image = mockup.copy()
        result_image.paste(decal, (x, y), decal)

        # Construct the output path
        output_path = os.path.join(output_folder, f'mockup_{decal_filename}')
        result_image.save(output_path)

# Define file paths
decal_folder =  "" # Replace with your 'processed' folder path
mockup_path =  "" # Replace with the path to your mockup image
output_folder = "" # Replace with your desired output folder path

decal_height = 2824  # Set this to your desired decal height
opacity = 254  # Adjust opacity here: 255 is fully opaque, 0 is fully transparent
rotation_angle = -15  # Adjust rotation angle here

# Place the decals
place_decal_on_mockup(decal_folder, mockup_path, output_folder, decal_height, opacity, rotation_angle)