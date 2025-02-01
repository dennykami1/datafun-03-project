"""
Clean and Process an Excel file to get population change for each penguin species.
Cleaned excel saved & a CSV file saved with population change for each species within
the specified years.

"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib

# Easy access to modern Excel files
import openpyxl

# Import from local project modules
from utils_logger import logger

# Read and manipulate Excel files
import pandas as pd

#####################################
# Declare Global Variables
#####################################

fetched_folder_name: str = "fetched_data"
processed_folder_name: str = "processed_data"

#####################################
# Define Functions
#####################################

def clean_excel_year(path: str, cleaned_path: str) -> None:
    """
    Clean the YEAR column in the Excel file by keeping only the first four digits.

    Args:
        path (str): The path to the Excel file.
        cleaned_path (str): The path where the cleaned Excel file will be saved.

    Returns:
        Excel file with cleaned YEAR
    """
    file_path = pathlib.Path(path).joinpath('Annual_Penguin_Census.xlsx')
    cleaned_file_path = pathlib.Path(cleaned_path).joinpath('cleaned_Annual_Penguin_Census.xlsx')

    try:
        logger.info(f"Reading Excel file from {file_path}...")

        # Load the Excel file
        df = pd.read_excel(file_path, engine="openpyxl")

        # Standardize column names
        df.columns = df.columns.str.strip().str.upper()  # Convert column names to uppercase for consistency

        if "YEAR" not in df.columns:
            logger.error("Error: 'YEAR' column not found in the Excel file.")
            return

        # Ensure YEAR column contains only the first 4 digits
        df["YEAR"] = df["YEAR"].astype(str).str[:4]

        # Convert YEAR back to integer (if valid)
        df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce").astype("Int64")

        # Save the cleaned file with a "cleaned_" prefix
        df.to_excel(cleaned_file_path, index=False, engine="openpyxl")

        logger.info(f"Cleaned YEAR column and saved to {cleaned_file_path}")

    except Exception as e:
        logger.error(f"Error processing Excel file: {e}")

def get_population_change(path: str, output_name: str, start_year: int, end_year: int) -> None:
    """
    Compute the population change for each penguin species between the start and end years.

    Args:
        path (str): The directory where the cleaned Excel file is stored and where the population change file will be saved.
        output_name (str): The name of the output CSV file.
        start_year (int): The starting year for comparison.
        end_year (int): The ending year for comparison.

    Returns:
        CSV file with population change for each penguin species.
    """
    cleaned_file_path = pathlib.Path(path).joinpath('cleaned_Annual_Penguin_Census.xlsx')
    cleaned_output_path = pathlib.Path(path).joinpath(output_name)  # Save the CSV file in the same folder

    logger.info(f"Reading cleaned Excel file from {cleaned_file_path}...")
    
    try:
        # Read the cleaned Excel file
        df = pd.read_excel(cleaned_file_path, engine='openpyxl')

        # Ensure column names are standardized
        df.columns = df.columns.str.strip().str.upper()

        if "YEAR" not in df.columns:
            logger.error("Error: 'YEAR' column not found in the cleaned Excel file.")
            return

        logger.info(f"Filtering data for years {start_year} and {end_year}...")

        # Filter data to only keep rows corresponding to start and end years
        df_filtered = df[df['YEAR'].isin([start_year, end_year])]

        if df_filtered.empty:
            logger.error(f"No data found for the specified years: {start_year} and {end_year}")
            return

        # Reshape the data to get population changes
        df_pivot = df_filtered.set_index('YEAR').T  # Transpose data to have species as rows
        df_pivot['Population_Change'] = df_pivot[end_year] - df_pivot[start_year]

        # Reset index to make the species column visible in CSV
        df_pivot.reset_index(inplace=True)
        df_pivot.rename(columns={'index': 'Species'}, inplace=True)

        # Save results to CSV in the same directory
        cleaned_output_path.parent.mkdir(parents=True, exist_ok=True)
        df_pivot[['Species', start_year, end_year, 'Population_Change']].to_csv(cleaned_output_path, index=False)

        logger.info(f"Population changes saved to {cleaned_output_path}")

    except Exception as e:
        logger.error(f"Error processing cleaned Excel file: {e}")

#####################################
# Define main() function
#####################################

def main():
    """ Clean & Process the Excel file to compute population change for each penguin species. """
    cleaned_path = processed_folder_name  # The folder where the cleaned file will be saved
    output_name = 'Penguin_Population_Change.csv'
    start_year = 2010
    end_year = 2014
    
    # First, clean the YEAR column in the Excel file and save the cleaned file in cleaned_path
    clean_excel_year(fetched_folder_name, cleaned_path)  # Pass the folder where the original file is located
    
    # Then, compute the population change based on the cleaned file located in cleaned_path
    get_population_change(cleaned_path, output_name, start_year, end_year)

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting Excel processing...")
    main()
    logger.info("Excel processing complete.")
