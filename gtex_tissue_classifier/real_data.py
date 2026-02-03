# Goal: Handles extraction, transformation and loading of raw GTEx source files. Used to build database for the full tool.
import pandas as pd

def parse_raw_gct(filepath):
    """
    Parses the .gct files downloaded from GTEx database.
    """
    pass

def compute_TPM(tissue_matrix):
    """
    Calculates median TPM vector for tissues in tissue matrix.
    """
    pass

def build_db(file_list):
    """
    Runs through tissue GCT files, computes median TPM values, outputs 'gtex_reference.csv' database.
    """
    pass