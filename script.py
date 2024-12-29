import argparse
import openeo
import json

# Ansi colorizations for better command line experience
RED = '\033[31m'
BLUE = '\033[34m'
RESET = '\033[0m' # called to return to standard terminal text color

def main (args) :

    try:
        # Connect to the Backend
        con = openeo.connect(args.backend_connection)
        
        # Authenticate to the service( using OpenID Connect)
        con.authenticate_oidc()

        # Parse parameters from command line argument
        params = dict(
            collection_name=args.collection,                  # The name of the collection
            spatial_extent = {                                # The geographocal place - Area of interest (boundng box)
                "west": args.west,
                "south": args.south,
                "east": args.east,
                "north": args.north
            },
            temporal_extent = [                               # Time range (start and end dates)
                args.start_date,
                args.end_date
            ],
            bands=args.bands.split(","),                      # Specific spectral bands (blue, red, NIR)
            max_cloud_cover=args.cloud_cover                  # Maximum cloud coverage percentage
        )

        # Load the collection into a DataCube
        # NOTE: Datacube is the main object of openeo
        datacube = con.load_collection(
            params["collection_name"],
            spatial_extent=params["spatial_extent"],
            temporal_extent=params["temporal_extent"],
            bands=params["bands"],
            max_cloud_cover=params["max_cloud_cover"]
        )

        # Execute the processing as a batch job
        # Send the processing job to the backend for execution. 
        con.list_file_formats()
        # Creating a new job at the back-end by sending the datacube information.
        job = datacube.create_job(title = args.jobs_title)
        job.start_and_wait()

        # Download results to the specified output directory
        job.get_results().download_files(args.output_dir)
        print(BLUE + f"Results downloaded to {args.output_dir}" + RESET)

    except openeo.rest.JobFailedException as e:
        # Handle job failure by catching the exception and printing an informative message
        print(RED + f"Error: The batch job failed to execute. Details: {str(e)}" + RESET)
        print(RED +"Possible causes include a too large spatial extent or a complex process graph." + RESET)
        print(RED +"Please try reducing the area of interest or modifying the job parameters." + RESET)
    
    except Exception as e:    
        # General exception handling for other errors
        print(RED + f"An unexpected error occurred: {str(e)}" + RESET)
    

if __name__ == '__main__':

    # Load arguments configuration from JSON file
    with open("./configs/arg_config.json", "r") as fobj:
        config = json.load(fobj)

    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description = "Extract data for the Dataset"
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