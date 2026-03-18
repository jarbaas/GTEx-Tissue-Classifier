# Goal: Generates the simulation data for unit tests and function testing. Can be used to validate math functions without needing full GTEx dataset.
import numpy as np
import pandas as pd

def generate_mock_tissues(filename: str, num_genes: int = 100, num_tissues: int = 50) -> None:
    """
    Creates a reference matrix with representative gene TPM values in rows and example tissues in columns, for testing package functions.
    
    Args:
        filename: str, path to save the simulated .gct file.
        num_genes: int, number of genes to simulate.
        num_tissues: int, number of tissue samples to simulate.
    """
    # Mock GTEx metadata above headers
    version = "#1.2"
    dimensions = f"{num_genes}\t{num_tissues}"
    # Headers in GTEx format
    names= [f"ENSG00000{i}" for i in range(num_genes)]
    descriptions = [f"Gene_{i}" for i in range(num_genes)]
    sample_ids = [f"GTEX-{i}" for i in range(num_tissues)]
    header = ["Name", "Description"] + sample_ids
    # Generate random TPM values with a log-normal distribution
    data = np.random.lognormal(mean=-1, sigma=1, size=(num_genes, num_tissues)) # Mean and sigma can be adjusted to modify TPM distribution
    with open(filename, 'w') as f:
        f.write(f"{version}" + "\n")
        f.write(f"{dimensions}" + "\n")
        f.write("\t".join(header) + "\n")
        for i in range(num_genes):
            row = f"{names[i]}\t{descriptions[i]}\t"
            values = "\t".join([f"{x:.5f}" for x in data[i]])
            f.write(row + values + "\n")
    print(f"Sample tissue matrix created at {filename}")

def generate_mock_sample(filename: str, num_genes: int = 100) -> None:
    """
    Creates an unknown sample matrix with representative genes in rows and TPM values in columns. Output is in CSV format. 
    
    Args:
        filename: str, path to save the simulated sample CSV file.
        num_genes: int, number of genes to simulate.
    """
    genes = [f"ENSG00000{i}" for i in range(num_genes)]
    tpm_vals = np.random.lognormal(mean=-1, sigma=1, size=num_genes) # Mean and sigma can be adjusted to modify TPM distribution 
    df = pd.DataFrame({'Gene': genes, 'TPM': tpm_vals})
    df.to_csv(filename, index=False)
    print(f"Mock sample created and saved to {filename}")