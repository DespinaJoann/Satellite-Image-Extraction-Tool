import os
import rasterio                         # A library for reading .tif formatted documents
import matplotlib.pyplot as plt         # A library for plotting, reading and saving images
import numpy as np                      # A library for handling arrays

def open_img(path_to_img):
    with rasterio.open(path_to_img) as src:
        band = src.read(1)
    return band

def convert(path_to_img, out_dir, date, idx):
    # Open the GeoTIFF image and extract its information
    with rasterio.open(path_to_img) as src:
        # Read all the bands of a Sentinel-2 image 
        img_data = src.read([1, 2, 3])  # (B02 (Blue), B04 (Red), B08 (NIR))

        # Get the dimensions of the image
        width, height = src.width, src.height

    # Convert the .tif image to RGB
    rgb_img = np.stack([img_data[0], img_data[1], img_data[2]], axis=-1)
    
    # Convert to float32 for better precision and scale to [0, 1]
    rgb_image = rgb_img.astype(np.float32)
    rgb_image = (rgb_image - np.min(rgb_image)) / (np.max(rgb_image) - np.min(rgb_image))
    
    # Scale to [0, 255] and convert to uint8
    rgb_image = (rgb_image * 255).astype(np.uint8)

    # Visualize the resulting image
    plt.imshow(rgb_image)
    plt.axis("off")
    plt.show()

    # Save the image to the output directory
    plt.imsave(f"{out_dir}/{date}_idx{idx}.png", rgb_image)

def convert_all(input_dir, out_dir, date):
    # Create the output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)

    # Loop through all files in the 'input_dir'
    for idx, filename in enumerate(os.listdir(input_dir)):
        if filename.endswith(".tif"):  # Check if the file is a .tif image
            path_to_img = os.path.join(input_dir, filename)
            convert(
                path_to_img=path_to_img,
                out_dir=out_dir,
                date=date,
                idx=str(idx + 1)
            )
    print("Conversion process from .tif to .png succeeded!")

# Test how it works
convert_all(
    "./results",            # Folder with the input .tif images
    "./imgs",               # Folder where the output RGB images will be saved
    "2024_12_29"            # Current Date (or another appropriate identifier)
)
