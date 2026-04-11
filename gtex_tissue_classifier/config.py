import os
import pandas as pd
from gtex_tissue_classifier.validation import validate_file_path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_file_data(relative_filepath: str) -> list:
    """
    Reads the data from a text file and returns it as a list of lines.

    Args:
        relative_filepath: str, path to text file relative to PROJECT_ROOT.

    Input: Text file with containing data written one entry per line.

    Output: Stripped list of lines from file. Empty list is returned if file is not found or an error occurs.
    """
    absolute_path = os.path.join(PROJECT_ROOT, relative_filepath)
    
    validate_file_path(absolute_path, None) 

    with open(absolute_path, "r") as file:
        data = [line.strip() for line in file if line.strip()]
        return data
