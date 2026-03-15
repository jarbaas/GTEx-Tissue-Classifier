import os
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_file_data(relative_filepath):
    """
    Reads the data from a text file and returns it as a list of lines.

    Args:
        relative_filepath: str, path to text file relative to PROJECT_ROOT.
    
    Input: Text file with containing data written one entry per line.

    Output: Stripped list of lines from file. Empty list is returned if file is not found or an error occurs.
    """
    absolute_path = os.path.join(PROJECT_ROOT, relative_filepath)

    try:
        with open(absolute_path, 'r') as file:
            data = [line.strip() for line in file if line.strip()]
        return data
    except FileNotFoundError:
        print(f"Error: The file '{absolute_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []