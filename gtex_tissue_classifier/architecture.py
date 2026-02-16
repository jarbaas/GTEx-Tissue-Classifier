# Goal: Manage user inputs, choose between simulation vs real data runs, manages data flow between downstream modules.
import os
import pandas as pd
from .simulation import generate_mock_sample
import argparse
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    """
    Decides between running the tool on simulated data or real data.
    """
    print("Package Installation Success")
    

def parse_arguments():
    """
    Uses argparse to understand flags on data such as '--input', '--output', '--mode'.
    """
    pass

def load_input(filepath):
    """
    Reads users CSV file, validates existence of "Gene" and "TPM" columns, returns Pandas DF. Note that the Gene column should contain Ensembl IDs in the format "ENSG00000X".

    Args:
        filepath: str, path to input CSV file.

    Input: CSV file with "Gene" and "TPM" columns.

    Output: Pandas DataFrame with gene names and TPM values.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file '{filepath}' was not found.")
    
    try:
        sample_df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")
    
    required_cols = {'Gene', 'TPM'}
    if not required_cols.issubset(sample_df.columns):
        missing = required_cols - set(sample_df.columns)
        raise ValueError(f"Input file missing required columns: {missing}")

    return sample_df

def validate_normalization(df):
    """
    Ensures input sample is TPM normalized and raises error if raw counts are detected.

    Args:
        df: Dataframe with "Gene" and "TPM" columns.

    Output: None, raises ValueError if TPM values are not valid.
    """
    if df['TPM'].dtype not in [float, int]:
        raise ValueError("TPM column must contain numeric values.")
    
    if (df['TPM'] < 0).any():
        raise ValueError("TPM values cannot be negative.")
    
    if (df['TPM'] > 1e6).any():
        raise ValueError("TPM values seem high, please check input data.")
    
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