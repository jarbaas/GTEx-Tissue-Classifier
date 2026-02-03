#  Goal: Purely numerical, accepts vectors and returns statistical scores
import pandas as pd

def calculate_spearman(vector, tissue_matrix):
    """
    Calculates correlation between input vector and tissue columns in the tissue matrix.
    """
    pass

def rank_matches(correlation_dict):
    """
    Sorts the correlation results in descending order to identify closest matches.
    """
    pass

def filter_variable_genes(df, n=2000):
    """
    Filters the gene lists in the tissue dataframe to the top 2000 most variable, 
    relying on unique genes to distinguish tissues.
    """
    pass