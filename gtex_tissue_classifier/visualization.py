# Goal: Converts the mathematical outputs in math module into graphs and images
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_correlations(ranked_tissues, output_path):
    """
    Uses matplotlib to generate a bar chart of the top five tissue matches.
    """
    top_5 = ranked_tissues[:5]
    tissues = [item[0] for item in top_5]
    correlations = [item[1] for item in top_5]
    plt.barh(tissues, correlations, height=0.5)
    plt.title('Highest Likelihood Tissue Matches')
    plt.xlabel('Spearman Correlation')
    plt.ylabel('Tissue Type')
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.savefig(f'{output_path}/tissue_rankings.png', dpi=300)
    plt.close()


def plot_marker_heatmap(sample_df, gct_matrix, top_tissue, output_path, gene_mapping=None):
    """
    Generates a heatmap comparing top markers of input samples to top markers 
    defining the closest matching tissue.
    """
    tissue_vector = gct_matrix[top_tissue].sort_values(ascending=False).head(50)
    sample_vector = sample_df.set_index('Gene')['TPM']
    sample_vector_filtered = sample_vector[sample_vector.index.isin(tissue_vector)]
    heatmap_df = pd.Dataframe({'Sample': sample_vector_filtered, f'GTEx Reference {top_tissue}': tissue_vector})
    heatmap_zscores = heatmap_df.apply(lambda x: (x - x.mean()) / x.std(), axis=1)
    
    if gene_mapping:
        heatmap_zscores.index = heatmap_zscores.index.map(gene_mapping).fillna(heatmap_zscores.index)
    
    plt.figure(figsize=(10,8))
    sns.heatmap(heatmap_zscores, 
                annot=True,
                cmap='RdBu_r',
                center=0,
                fmt='.2f')
    plt.ylabel('Marker Genes')
    plt.xlabel('Data Source')
    plt.title(f'Top 50 Marker Gene Expression, Sample v {top_tissue}')
    plt.tight_layout()
    plt.savefig(f'{output_path}/top_marker_heatmap.png', dpi=300)
    plt.close()

def write_summary_report(results, filename):
    """
    Outputs the final tissue prediction, confidence score and/or any warnings into an html file.
    """
    pass