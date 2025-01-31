"""
Process a CSV file on Global Population Data by year to create a chart for the defined country county.
"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib

# Import from external packages
import pandas as pd
import matplotlib.pyplot as plt

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

def generate_population_trend_chart(country_name: str) -> None:
    """
    Generate a population trend chart for the specified country and save it as a PNG.

    Args:
        country_name (str): The name of the country for which the chart will be generated.

    Returns:
        PNG file
    """
    # Load data from the CSV file
    try:
        file_path = pathlib.Path(fetched_folder_name).joinpath("global_population.csv")
        df = pd.read_csv(file_path)

        # Filter the data for the specified country
        country_data = df[df['Country Name'] == country_name]

        if country_data.empty:
            logger.error(f"No data found for country: {country_name}")
            return

        # Determine the unit based on the largest population value if not provided
        max_population = country_data['Value'].max()
        if max_population >= 1e9:
            unit = "billions"
        elif max_population >= 1e6:
            unit = "millions"
        else:
            unit = "thousands"

        # Define a mapping for units
        unit_mapping = {
            "billions": 1e9,
            "millions": 1e6,
            "thousands": 1e3
        }
        
        logger.info(f"Population unit set to: {unit}")

        # Create the population trend chart
        plt.figure(figsize=(10, 6))
        plt.plot(country_data['Year'], country_data['Value'], marker='o')
        plt.title(f"Population Trend for {country_name}")
        plt.xlabel("Year")
        plt.ylabel(f"Population ({unit.capitalize()})")
        plt.grid(True)

        # Save the chart to the processed_data folder
        output_path = pathlib.Path(processed_folder_name).joinpath(f"{country_name}_population_trend.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path)
        plt.close()

        logger.info(f"Population trend chart saved as {output_path}")
    except Exception as e:
        logger.error(f"An error occurred while generating the chart: {e}")

#####################################
# Define main() function
#####################################

def main():
    """
    Main function to demonstrate generating a population trend chart for a country.
    """
     # Example usage: Set the desired country name here
    country = "United States"
    generate_population_trend_chart(country)

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting CSV processing...")
    main()
    logger.info("CSV processing complete.")
