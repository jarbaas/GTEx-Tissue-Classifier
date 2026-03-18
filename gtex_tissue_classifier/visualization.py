# Goal: Converts the mathematical outputs in math module into graphs and images
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_correlations(
    ranked_tissues: list[tuple[str, float]], output_path: str
) -> None:
    """
    Uses matplotlib to generate a bar chart of the top five tissue matches.
    """
    top_5 = ranked_tissues[:5]
    tissues = [item[0] for item in top_5]
    correlations = [item[1] for item in top_5]
    plt.barh(tissues, correlations, height=0.5)
    plt.title("Highest Likelihood Tissue Matches")
    plt.xlabel("Spearman Correlation")
    plt.ylabel("Tissue Type")
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.savefig(f"{output_path}/tissue_rankings.png", dpi=300)
    plt.close()


def plot_marker_heatmap(
    sample_df: pd.DataFrame,
    gct_matrix: pd.DataFrame,
    top_tissue: str,
    output_path: str,
    gene_mapping: dict[str, str] | None = None,
) -> None:
    """
    Generates a heatmap comparing top markers of input samples to top markers
    defining the closest matching tissue.
    """
    tissue_vector = gct_matrix[top_tissue].sort_values(ascending=False).head(50)
    sample_vector = sample_df.set_index("Gene")["TPM"]
    sample_vector_filtered = sample_vector[
        sample_vector.index.isin(tissue_vector.index)
    ]
    heatmap_df = pd.DataFrame(
        {
            "Sample": sample_vector_filtered,
            f"GTEx Reference {top_tissue}": tissue_vector,
        }
    )
    heatmap_normalized = heatmap_df.apply(np.log1p)

    if gene_mapping:
        heatmap_normalized.index = heatmap_normalized.index.map(gene_mapping).fillna(heatmap_normalized.index)  # type: ignore

    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_normalized, annot=True, cmap="viridis", fmt=".1f")
    plt.ylabel("Marker Genes")
    plt.xlabel("Data Source")
    plt.title(f"Top 50 Marker Gene Expression, Sample v {top_tissue}")
    plt.tight_layout()
    plt.savefig(f"{output_path}/top_marker_heatmap.png", dpi=300)
    plt.close()


def write_summary_report(results, filename):
    """
    Outputs the final tissue prediction, confidence score and/or any warnings into an html file.
    """
    pass
