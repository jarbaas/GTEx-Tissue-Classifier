# Goal: Generates the simulation data for unit tests and function testing. Can be used to validate math functions without needing full GTEx dataset.
import numpy as np
import pandas as pd
import os
import random
from gtex_tissue_classifier.config import PROJECT_ROOT


def generate_mock_tissues(
    filename: str, num_genes: int = 100, num_tissues: int = 50
) -> None:
    """
    Creates a reference matrix with representative gene TPM values in rows and example tissues in columns, for testing package functions.

    Args:
        filename: str, path to save the simulated .gct file.
        num_genes: int, number of genes to simulate.
        num_tissues: int, number of tissue samples to simulate.
    """
    ref_path = os.path.join(PROJECT_ROOT, "data", "master_reference_matrix.csv")

    try:
        ref_df = pd.read_csv(ref_path, index_col=0)
        # Sample desired number of real gene and tissue names from the database
        sampled_genes = ref_df.sample(n=min(num_genes, len(ref_df)))
        data_matrix = sampled_genes.sample(
            n=min(num_tissues, len(ref_df.columns)), axis=1
        )

        # Build matrix
        names = data_matrix.index.tolist()
        descriptions = [f"Gene_{i}" for i in range(len(names))]
        sample_ids = data_matrix.columns.tolist()
        data = data_matrix.values
        num_genes, num_tissues = data.shape

    except FileNotFoundError:
        # Ensembl IDs and GTEx tissue classifiers are randomly generated if GTEx reference not present
        names = [f"ENSG00000{i}" for i in range(num_genes)]
        descriptions = [f"Gene_{i}" for i in range(num_genes)]
        sample_ids = [f"GTEX-{i}" for i in range(num_tissues)]
        # Mean and sigma can be adjusted to modify TPM distribution
        data = np.random.lognormal(mean=-1, sigma=1, size=(num_genes, num_tissues))

    # Mock GTEx metadata above headers
    version = "#1.2"
    dimensions = f"{num_genes}\t{num_tissues}"
    header = ["Name", "Description"] + sample_ids

    with open(filename, "w") as f:
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
    ref_path = os.path.join(PROJECT_ROOT, "data", "master_reference_matrix.csv")

    try:
        ref_df = pd.read_csv(ref_path, index_col=0)
        # Selects random tissue from GTEx reference and picks the requested number of genes
        target_tissue = random.choice(ref_df.columns.tolist())
        base_vector = ref_df[target_tissue].sample(n=min(num_genes, len(ref_df)))
        genes = base_vector.index.tolist()

        # Apply biological noise to TPM values
        log_expr = np.log1p(base_vector)
        noise = np.random.normal(loc=0.0, scale=0.5, size=len(log_expr))
        noisy_log = np.clip(log_expr + noise, a_min=0, a_max=None)
        tpm_vals = np.asarray(np.expm1(noisy_log))

    except FileNotFoundError:
        # Ensembl IDs and random values are generated if GTEx reference not present
        genes = [f"ENSG00000{i}" for i in range(num_genes)]
        # Mean and sigma can be adjusted to modify TPM distribution
        tpm_vals = np.random.lognormal(mean=-1, sigma=1, size=num_genes)

    df = pd.DataFrame({"Gene": genes, "TPM": tpm_vals})
    df.to_csv(filename, index=False)
    print(f"Mock sample created and saved to {filename}")
