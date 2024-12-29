
# Satellite-Image-Extraction-Tool

This repository contains a Python project that leverages the [`openeo`](https://openeo.org/documentation/1.0/) library to extract satellite data. It processes the data into GeoTIFF images for a specified area of interest and optionally converts these GeoTIFFs into RGB PNG files for easier visualization.

## Project Structure

- **`/config`**: The folder containing the configurations for some automations.
    - **`/config/arg_config.json`**: The configuration of the command-line arguments for the script's task execution.
    - - **`/config/cnv_config.json`**: The configuration of the command-line arguments for the convert's task execution.
- **`script.py`**: The main file that extracts the GeoTIFF images for the specified area of interest.
- **`convert.py`**: A script to convert the extracted GeoTIFF images to RGB PNG files.

- **`output/`**: A folder where the GeoTIFF results will be saved.
- **`imgs/`**: A folder where the image conversions (GeoTIFF to RGB PNG) will be stored.
- **`results/`**: A folder for any additional results.

## Setup

To run this project, you'll need to set up a few folders locally:

1. **`output/`**: Create a folder for storing GeoTIFF results.
2. **`imgs/`**: Create a folder for storing converted image files (RGB PNG).

Ensure you have the required dependencies installed. You can do this by creating a virtual environment and installing the necessary libraries.

```zsh
# Create a virtual environment (optional but recommended)
python -m venv myenv
source myenv/bin/activate  # On Windows, use myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Run the Script

Once you've set up the environment and created the necessary folders, you can run the script to extract the data. Below is an example of how to use `script.py` to get Sentinel-2 data from a specified region and time period.

```zsh
python script.py --backend_connection "openeo.dataspace.copernicus.eu" \
    --collection "SENTINEL2_L2A" \
    --west 5.14 --south 51.17 --east 5.17 --north 51.19 \
    --start_date "2021-02-01" --end_date "2021-04-30" \
    --bands "B02,B04,B08" --cloud_cover 20 \
    --output_dir "./output" --jobs_title "Sentinel Data Extraction Job"
```

### Parameters:
- **`--backend_connection`**: The URL of the OpenEO backend to connect to.
- **`--collection`**: The collection of satellite data to retrieve (e.g., `"SENTINEL2_L2A"`).
- **`--west`, `--south`, `--east`, `--north`**: The geographic coordinates of the area of interest (bounding box).
- **`--start_date`, `--end_date`**: The time range for the data you want to extract.
- **`--bands`**: A comma-separated list of spectral bands (e.g., `"B02,B04,B08"`).
- **`--cloud_cover`**: The maximum allowable cloud cover percentage for the images.
- **`--output_dir`**: The directory where the extracted GeoTIFF files will be stored.
- **`--jobs_title`**: The title for the job that will be created on the backend.

## Convert GeoTIFF to RGB PNG

If you want to convert the extracted GeoTIFF files to RGB PNG format, you can run the `convert.py` script. The converted images will be saved in the `imgs/` folder.

```zsh
python convert.py --input_dir "./results" --out_dir "./imgs" --date "2024-12-29"
```

## Dependencies

- `openeo`: The library for interacting with OpenEO backends.
- `numpy`: Required for data manipulation.
- `rasterio`: To read and write GeoTIFF files.
- `Pillow`: For image processing (GeoTIFF to PNG conversion).
- `matplotlib`: Optional, for visualizing the images.

## License

This project is licensed under the MIT License - see the [LICENSE]() file for details.

