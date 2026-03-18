# Goal: Manage user inputs, choose between simulation vs real data runs, manages data flow between downstream modules.
import os
import pandas as pd
from .config import PROJECT_ROOT, read_file_data
from gtex_tissue_classifier import simulation, real_data, math_logic, visualization
from gtex_tissue_classifier.validation import InputValidation
import argparse
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def parse_arguments() -> argparse.Namespace:
    """
    Uses argparse to understand flags on data such as '--input', '--output', '--mode'.
    """
    parser = argparse.ArgumentParser(description="Welcome to GTEx Tissue Classifier. Match an RNA sequencing sample of uknown tissue origin to the most likely tissue in the GTEx database.")
    parser.add_argument(
        '-m', '--mode',
        choices=['real', 'simulated'],
        required=True,
        help="Specify 'real' to begin process with inputted user data or specify 'simulated' to run the tool with simulated sample data."
    )
    parser.add_argument(
        '-i', '--input',
        type=str,
        help="Filepath to the CSV file containing the input RNA sequencing data. This argument is required in 'real'."
    )
    parser.add_argument(
        '-r', '--reference',
        type=str,
        help="Optional filepath to custom reference matrix, otherwise defaults to bundled GTEx reference .gct file."
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='.',
        help="Filepath to save output plots and results, set to current path by default."
    )

    return parser.parse_args()

def main() -> None:
    """
    Decides between running the tool on simulated data or real data.
    """
    print("Package Installation Success")
    
    args=parse_arguments()

    os.makedirs(args.output, exist_ok=True)

    gene_map = None

    # Simulation branch
    if args.mode == 'simulated':
        print("Running in simulated mode. Mock data generation commencing.")
        
        ref_path = os.path.join(args.output, 'sample_gtex.gct')
        simulation.generate_mock_tissues(ref_path, num_genes=100, num_tissues=50)
        
        sample_path = os.path.join(args.output, 'mock_sample.csv')
        simulation.generate_mock_sample(sample_path, num_genes=100)

        print(f"Mock data generated in '{args.output}'.")

    # Real branch
    elif args.mode == 'real':
        print("Running in real mode. Input validation commencing.")
        

        if not args.input:
            print("Error- no '--input' flag entered. This flag must be specified in real mode.")
            sys.exit(1)
        
        sample_path = args.input
        ref_path = args.reference

        if not ref_path:
            ref_path = os.path.join(PROJECT_ROOT,'data','processed','master_reference_matrix.csv')
            print("No custom GTEx reference file provided. Defaulting to bundled file.")

        gene_map = real_data.extract_gene_mapping(ref_path)

    print(f"Loading reference GTEx matrix from {ref_path}.")
    gct_matrix = real_data.parse_raw_gct(ref_path)

    print(f"Loading input sample from {sample_path}.")
    sample_df = load_input(sample_path)
    
    print("Running input validation.")
    validator = InputValidation(sample_df, gct_matrix)
    sample_df = validator.run_all_validations()
    
    print("Calculating Spearman correlations.")
    corr_dict = math_logic.calculate_spearman(sample_df, gct_matrix)

    print("Ranking matches and generating output files.")
    ranked_tissues = math_logic.rank_matches(corr_dict)
    visualization.plot_correlations(ranked_tissues, args.output)

    top_tissue = ranked_tissues[0][0]
    visualization.plot_marker_heatmap(
        sample_df, 
        gct_matrix, 
        top_tissue, 
        args.output, 
        gene_mapping=gene_map
    )

    print(f"Tissues successfully ranked. Top match is {top_tissue}. Results written to {args.output}.")

def load_input(filepath: str) -> pd.DataFrame:
    """
    Reads users CSV file, validates existence of "Gene" and "TPM" columns, returns Pandas DF. Note that the Gene column should contain Ensembl IDs in the format "ENSG00000X".

    Args:
        filepath: str, path to input CSV file.

    Input: CSV file with "Gene" and "TPM" columns.

    Output: Pandas DataFrame with gene names and TPM values.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file '{filepath}' was not found.")
    
    try:
        sample_df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")
    
    required_cols = {'Gene', 'TPM'}
    if not required_cols.issubset(sample_df.columns):
        missing = required_cols - set(sample_df.columns)
        raise ValueError(f"Input file missing required columns: {missing}")

    return sample_df    

if __name__ == "__main__":
    main()    