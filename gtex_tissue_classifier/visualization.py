# Goal: Converts the mathematical outputs in math module into graphs and images
import matplotlib.pyplot as plt
import numpy as np

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


def plot_marker_heatmap(user_vector, ref_vector):
    """
    Generates a heatmap comparing top markers of input samples to top markers 
    defining the closest matching tissue.
    """
    pass

def write_summary_report(results, filename):
    """
    Outputs the final tissue prediction, confidence score and/or any warnings into an html file.
    """
    pass