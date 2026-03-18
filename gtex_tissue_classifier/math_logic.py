#  Goal: Numerical, perform important statistical tests and filter results.
import pandas as pd
import numpy as np


def filter_variable_genes(df: pd.DataFrame, n: int = 2000) -> pd.DataFrame:
    """
    Filters the gene lists in the tissue DataFrame to the top 2000 most variable,
    relying on unique genes to distinguish tissues.
    """
    vst_df = np.log2(df + 1)
    gene_variance = vst_df.var(axis=1)
    top_genes = gene_variance.nlargest(n).index
    filtered_df = df.loc[top_genes]
    return filtered_df


def calculate_spearman(
    sample_df: pd.DataFrame, tissue_matrix: pd.DataFrame
) -> dict[str, float]:
    """
    Calculates Spearman correlation between sample_df and tissue columns in the tissue matrix.

    Args:
        sample_df: DataFrame,  with gene column and TPM column.
        tissue_matrix: DataFrame with genes in rows, tissue samples in columns, and TPM values as entries.
    """
    sample_series = sample_df.set_index("Gene")["TPM"]
    matched_genes = sample_series.index.intersection(tissue_matrix.index)
    if len(matched_genes) == 0:
        raise ValueError("No matching genes found between sample and tissue matrix.")

    aligned_sample = sample_series.loc[matched_genes]
    aligned_tissue = tissue_matrix.loc[matched_genes]

    corr_matrix = aligned_tissue.corrwith(aligned_sample, method="spearman")
    corr_dict = corr_matrix.to_dict()
    return corr_dict  # type: ignore


def rank_matches(corr_dict: dict[str, float]) -> list[tuple[str, float]]:
    """
    Sorts the correlation results in descending order to identify closest matches.

    Args:
        corr_dict: Dictionary, maps tissue names to their Spearman correlation scores.

    """
    ranked_tissues = sorted(corr_dict.items(), key=lambda x: x[1], reverse=True)
    return ranked_tissues
