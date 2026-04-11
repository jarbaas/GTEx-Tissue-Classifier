# Goal: Converts the mathematical outputs in math module into graphs and images
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_correlations(
    ranked_tissues: list[tuple[str, float]], output_path: str
) -> None:
    """
    Uses matplotlib to generate a bar chart of the top five tissue matches.

    Args:
        ranked_tissues: list[tuple[str, float]], input list of tuples with top tissue matches and their spearman correlation values
        output_path: str, location for correlation plots to be saved
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
    plt.savefig(os.path.join(output_path, "tissue_rankings.png"), dpi=300)
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

    Args:
        sample_df: pd.DataFrame, DataFrame containing the input sample TPM values
        gct_matrix: pd.DataFrame, DataFrame containing the GTEx reference TPM values
        top_tissue: str, name of the top tissue match determined by the tool
        output_path: str, location for marker heatmap to be saved
        gene_mapping: dict[str, str] | None = None, dictionary of Ensembl ID to gene name mapping, or None if not provided
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
        # dictionary keys need to be stripped like with gtex inputs
        clean_mapping = {str(k).split('.')[0]: v for k, v in gene_mapping.items()}
        # map symbols or leave as ensembl ID if mapping not found
        heatmap_normalized.index = heatmap_normalized.index.map(lambda x: clean_mapping.get(x, x))

    plt.figure(figsize=(10, 12))
    ax = sns.heatmap(heatmap_normalized, annot=True, cmap="viridis", fmt=".1f")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, va="center", fontsize=9)
    plt.ylabel("Marker Genes")
    plt.xlabel("Data Source")
    plt.title(f"Top 50 Marker Gene Expression, Sample v {top_tissue}")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "tissue_rankings.png"), dpi=300)
    plt.close()


def write_summary_report(results: list[tuple[str, float]], filename: str) -> None:
    """
    Outputs the final tissue prediction, confidence score and/or any warnings into an html file.

    Args:
        results: A sorted list of tuples from rank_matches containing (tissue_name, correlation_score).
        filename: The complete output filepath for the HTML file.
    """
    if not results:
        raise ValueError("No matching tissues, unable to generate report.")

    # Extract report data from results
    top_tissue = results[0][0]
    confidence = results[0][1]
    top_5 = results[:5]

    # Build HTML document 
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GTEx-Tissue-Classifier Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
            h1 {{ color: #2c3e50; }}
            .highlight {{ color: #27ae60; font-weight: bold; }}
            table {{ border-collapse: collapse; width: 50%; margin-top: 20px; }}
            th, td {{ border: 1px solid #dddddd; padding: 10px; text-align: left; }}
            th {{ background-color: #f8f9fa; }}
        </style>
    </head>
    <body>
        <h1>Tissue Match Summary</h1>
        <p>The highest correlating tissue match is: <span class="highlight">{top_tissue}</span></p>
        <p>Spearman Correlation Score: <strong>{confidence:.4f}</strong></p>

        <h2>Top 5 Closest Matches</h2>
        <table>
            <tr>
                <th>Tissue</th>
                <th>Spearman Score</th>
            </tr>
    """

    # Generate a top 5 table for report
    for tissue, score in top_5:
        html_content += f"""
            <tr>
                <td>{tissue}</td>
                <td>{score:.4f}</td>
            </tr>
        """

    # Close the report
    html_content += """
        </table>
    </body>
    </html>
    """

    # Save to specified path
    with open(filename, 'w') as file:
        file.write(html_content)
    
