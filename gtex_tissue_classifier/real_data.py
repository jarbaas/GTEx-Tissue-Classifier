# Goal: Handles extraction, transformation and loading of raw GTEx source files. Used to build database for the full tool.
import os
from .architecture import read_file_data, PROJECT_ROOT
import pandas as pd
import requests

def download_gtex_data(tissue_filepath, output_dir):
    """
    Downloads .gct files for all tissues from the GTEx portal. Designate tissue list location in simple filepath argument, eg. /configs/tissue_list.txt.

    Args:
        tissue_filepath: str, file path of text file listing GTEx tissues to download.
    
    Input: Text file with list of GTEx tissues to download, one tissue per line.
        
    Output: Downloads .gct files for requested tissues to specified directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    base_url = "https://storage.googleapis.com/adult-gtex/bulk-gex/v11/rna-seq/tpms-by-tissue"
    tissues = read_file_data(tissue_filepath)
    for tissue in tissues:
        print(f"Downloading {tissue} data...")
        url = f"{base_url}/gene_tpm_v11_{tissue}.gct.gz"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(os.path.join(output_dir, f"{tissue}.gct.gz"), 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Failed to download {tissue} data. Status code: {response.status_code}")
    print("Download complete.")


def parse_raw_gct(filepath):
    """
    Parses a GTEx .gct file and returns DataFrame with genes in rows, tissues in columns, and TPM values as entries. 

    Args:
        filepath: str, path to the .gct file to be parsed.
    
    Input: GTEx .gct file
            
    Output: tissue_matrix: DataFrame with genes in rows, tissue samples in columns, and TPM values as entries.
    """
    tissue_matrix = pd.read_csv(filepath, sep='\t', skiprows=2)
    if 'Name' in tissue_matrix.columns:
        tissue_matrix.set_index('Name', inplace=True)
    if 'Description' in tissue_matrix.columns:
        tissue_matrix.drop(columns=['Description'], inplace=True)
    return tissue_matrix

def compute_TPM(tissue_matrix):
    """
    Calculates median TPM column for tissues in tissue matrix.

    Args:
        tissue_matrix: DataFrame, with genes in rows, tissue samples in columns, and TPM values as entries.

    Ouptput: tissue_matrix with 'Median_TPM' column added.
    """
    sample_cols = [col for col in tissue_matrix.columns if col.startswith("GTEX-")]
    tissue_matrix['Median_TPM'] = tissue_matrix[sample_cols].median(axis=1, skipna=True)
    
    return tissue_matrix

