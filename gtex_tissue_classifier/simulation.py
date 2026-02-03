# Goal: Generates the simulation data for unit tests and function testing. Can be used to validate math functions without needing full GTEx dataset.
import numpy as np
import pandas as pd

def generate_mock_tissues(rows=100, cols=5):
    """
    Creates a reference matrix with representative gene TPM values in rows and example tissues in columns.
    """
    pass

def generate_mock_sample(target_tissue, noise):
    """
    Creates an unknown sample matrix with representative genes in rows and TPM values in columns. 
    Gaussian noise can be specified in args to verify algorithmic handling.
    """
    pass