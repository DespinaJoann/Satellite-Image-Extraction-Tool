import os                          # OS functions to create directories and handle file paths
import rasterio                    # Read and manipulate GeoTIFF images (satellite data)
import matplotlib.pyplot as plt    # Visualize image data and save as PNG
import numpy as np                 # Handle image data as arrays (for processing and scaling)
import json                        # Load configuration settings (e.g., input/output paths)
import argparse                    # Parse command-line arguments (for user input)


def open_img(path_to_img):
    with rasterio.open(path_to_img) as src:
        band = src.read(1)
    return band

def convert(path_to_img, out_dir, date, idx):
    # Open the GeoTIFF image and extract its information
    with rasterio.open(path_to_img) as src:
        # Read all the bands of a Sentinel-2 image (B02 (Blue), B04 (Red), B08 (NIR))
        img_data = src.read([1, 2, 3])  # Sentinel-2 Bands (1 - Blue, 2 - Green, 3 - Red, etc.)

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

def main(args):
    # Create the output directory if it doesn't exist
    os.makedirs(args.out_dir, exist_ok=True)

    # Loop through all files in the 'input_dir'
    for idx, filename in enumerate(os.listdir(args.input_dir)):  # Use args.input_dir instead of input_dir
        if filename.endswith(".tif"):  # Check if the file is a .tif image
            path_to_img = os.path.join(args.input_dir, filename)
            convert(
                path_to_img=path_to_img,
                out_dir=args.out_dir,
                date=args.date,
                idx=str(idx + 1)
            )
    print("Conversion process from .tif to .png succeeded!")

if __name__ == '__main__':
    # Load arguments configuration from JSON file
    with open("./configs/cnv_config.json", "r") as fobj:
        config = json.load(fobj)

    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Convert .tif to .png"
    )

    # Add arguments to parser by iterating over the configuration list
    for arg in config["arguments"]:
        # Convert 'str' and 'int' from JSON to actual Python types
        arg_type = str if arg["type"] == "str" else float if arg["type"] == "float" else int
        parser.add_argument(
            arg["name"], 
            type=arg_type, 
            required=arg["required"], 
            default=arg.get("default"), 
            help=arg["help"]
        )

    # Parse arguments and run the main function
    args = parser.parse_args()
    main(args)
