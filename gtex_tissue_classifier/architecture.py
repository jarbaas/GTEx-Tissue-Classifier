# Goal: Manage user inputs, choose between simulation vs real data runs, manages data flow between downstream modules.
import pandas as pd
import os
import argparse
import sys

def main():
    """
    Decides between running the tool on simulated data or real data.
    """
    print("Package Installation Success")
    pass

def parse_arguments():
    """
    Uses argparse to understand flags on data such as '--input', '--output', '--mode'.
    """
    pass

def load_input(filepath):
    """
    Reads users CSV file, validates existence of "Gene" and "TPM" columns, returns Pandas DF.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file '{filepath}' was not found.")
    
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")
    
    required_cols = {'Gene', 'TPM'}
    if (df.columns) not in required_cols:
        raise ValueError(f"Input file missing required columns: {required_cols}")

    return df

def validate_normalization(df):
    """
    Ensures input sample is TPM normalized and raises error if raw counts are detected.
    """
    pass