"""
Process a JSON file to find statistics for the United States. Write the calculated statistics to a txt file.



# Example JSON data:

 [
    {
        "page": 1,
        "pages": 1,
        "per_page": 5000,
        "total": 64,
        "sourceid": "2",
        "lastupdated": "2025-01-28"
    },
    [
        {
            "indicator": {
                "id": "SP.POP.TOTL",
                "value": "Population, total"
            },
            "country": {
                "id": "US",
                "value": "United States"
            },
            "countryiso3code": "USA",
            "date": "2023",
            "value": 334914895,
            "unit": "",
            "obs_status": "",
            "decimal": 0
        },

"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import json

# Import from local project modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

fetched_folder_name: str = "fetched_data"
processed_folder_name: str = "processed_data"

#####################################
# Define Functions
#####################################

def process_json_file(input_path: str, output_name: str) -> None:
    """
    Process a JSON file to find statistics for the United States. 

    Args:
        input_path (str): The folder containing the input JSON file.
        output_name (str): The name of the output txt file that will be saved to processed_folder_name.

    Returns:
        None
    """
    # Load data from the JSON file
    try:
        file_path = pathlib.Path(fetched_folder_name).joinpath("USA_Population.json")
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return
    except json.JSONDecodeError as json_err:
        logger.error(f"JSON decoding error: {json_err}")
        return

    # The actual population data is in the second item in the list
    population_data = data[1]  # Extract population data

    # Filter out entries without the 'value' key
    filtered_data = [x for x in population_data if 'value' in x]

    # Now, perform the max and min operations on the filtered data
    if filtered_data:  # Ensure there's at least one item left after filtering
        max_population = max(filtered_data, key=lambda x: x['value'])
        min_population = min(filtered_data, key=lambda x: x['value'])
        rate_of_change = (max_population['value'] - min_population['value']) / len(filtered_data)
    else:
        logger.warning("No data with 'value' key found.")
        return

    # Write the calculated statistics to a text file
    output_file = pathlib.Path(processed_folder_name).joinpath("us_population_stats.txt")
    with open(output_file, "w") as file:
        file.write(f"Maximum Population: {max_population['value']} in {max_population['date']}\n")
        file.write(f"Minimum Population: {min_population['value']} in {min_population['date']}\n")
        file.write(f"Average Rate of Change: {rate_of_change:.2f} per year\n")

    logger.info(f"Statistics for the United States written to {output_file}")

#####################################
# Define main() function
#####################################
def main():
   
# Define the input folder and the name of the output file
    input_folder = "fetched_data"  # Example input folder where your JSON file is located
    output_file_name = "us_population_statistics.txt"  # Output text file with the statistics

    # Call the process_json_file function to process the JSON and generate statistics
    process_json_file(input_folder, output_file_name)

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting JSON processing...")
    main()
    logger.info("JSON processing complete.")