"""
This script reads a text file, counts the frequencies of all words (ignoring stop words),
saves the word frequencies to a CSV file, and creates a word cloud image.
"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib

#create word cloud
from wordcloud import WordCloud

#count frequency of words
from collections import Counter

# Import from local project modules
from utils_logger import logger

#data manipulation
import pandas as pd

#find words in text
import re

#plotting
import matplotlib.pyplot as plt

#####################################
# Declare Global Variables
#####################################

fetched_folder_name: str = "fetched_data"
processed_folder_name: str = "processed_data"

#####################################
# Define Functions
#####################################

STOP_WORDS = set([
    "the", "and", "a", "i", "of", "to", "in", "for", "on", "at", "with", "as", "by", "an", "this", "that", "which", 
    "it", "be", "are", "were", "was", "have", "has", "had", "not", "but", "or", "so", "for", "from", "because", "about", 
    "he", "you", "his", "her", "they", "them", "we", "us", "our", "my", "me", "she", "their", "there", "what", "when", 
    "where", "who", "whom", "why", "how", "is", "if", "all", "any", "can", "will", "would", "could", "should", "shall", 
    "do", "does", "did", "done", "no", "yes", "up", "down", "out", "in", "over", "under", "again", "further", "then", 
    "once", "here", "such", "only", "own", "same", "than", "too", "very", "most", "more", "other", "some", "few", "many",
    "s", "t", "him", "into", "its", "those", "these", "both", "each", "other", "another", "some", "much", "many", "little",
    "said"
])

def count_word_frequencies(file_path: pathlib.Path) -> Counter:
    """
    Count the frequencies of all words in a text file (case-insensitive), ignoring stop words.

    Args:
        file_path (pathlib.Path): The path to the text file to process.  

    Returns:
        Counter: A Counter object containing word frequencies.
    """
    try:
        with file_path.open('r', encoding='utf-8') as file:  # Specify encoding to avoid decoding errors
            content: str = file.read()
            words = re.findall(r'\w+', content.lower())  # Extract words and make them lowercase
            # Remove stop words
            filtered_words = [word for word in words if word not in STOP_WORDS]
            word_frequencies = Counter(filtered_words)  # Count occurrences of each word
            return word_frequencies
    except Exception as e:
        logger.error(f"Error reading text file: {e}")
        return Counter()

def save_word_frequencies_to_df(word_frequencies: Counter) -> pd.DataFrame:
    """
    Convert the word frequencies into a DataFrame and save it to a CSV file.

    Args:
        word_frequencies (Counter): A Counter object containing word frequencies.    

    Returns:
        pd.DataFrame: The DataFrame containing word frequencies.
    """
    logger.info("Converting word frequencies to DataFrame...")
    df = pd.DataFrame(word_frequencies.items(), columns=["Word", "Frequency"])
    df = df.sort_values(by="Frequency", ascending=False).reset_index(drop=True)
    logger.info("Word frequencies converted to DataFrame.")
    
    # Save the DataFrame to a CSV file
    save_path = pathlib.Path(processed_folder_name).joinpath("word_frequencies.csv")
    df.to_csv(save_path, index=False)
    logger.info(f"Word frequencies saved to: {save_path}")
    
    return df


def create_word_cloud(word_frequencies: Counter) -> None:
    """
    Create a word cloud from the word frequencies and save it as a PNG file.

    Args:
        word_frequencies (Counter): A Counter object containing word frequencies.

    Returns:
        PNG file
    """
    logger.info("Creating word cloud...")
    word_cloud = WordCloud(background_color='white').generate_from_frequencies(word_frequencies)
    plt.figure()
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save the word cloud before showing it
    save_path = pathlib.Path(processed_folder_name).joinpath("word_cloud.png")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    logger.info(f"Word cloud saved to: {save_path}")

#####################################
# Define main() function
#####################################

def main():
    """
    Main function to demonstrate processing a text file and creating a word cloud.
    """
    logger.info("Starting text processing...")
    
    # Specify the path to the text file
    file_path = pathlib.Path(fetched_folder_name).joinpath('great_gatsby.txt')
    word_frequencies = count_word_frequencies(file_path)
    save_word_frequencies_to_df(word_frequencies)
    create_word_cloud(word_frequencies)
    
    logger.info("Text processing complete.")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting text processing...")
    main()
    logger.info("Text processing complete.")
