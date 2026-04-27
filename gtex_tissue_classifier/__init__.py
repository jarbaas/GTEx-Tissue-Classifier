"""
GTEx-Tissue-Classifier
A bioinformatics tool for identifying the tissue of origin for RNA-seq samples
based on the GTEx V11 Tissue Database.
"""

__version__ = "1.0.0"
__author__ = "Jared Baas"

from .validation import InputValidation, validate_file_path, validate_output_directory
from .math_logic import calculate_spearman
from .visualization import plot_marker_heatmap
