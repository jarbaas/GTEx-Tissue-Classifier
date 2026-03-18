# Snakemake wrapper to process GTEx .gct tissue file into a DataFrame, calculate median TPM values, and prepare for loading into master .CSV file.
import pandas as pd
from gtex_tissue_classifier.real_data import parse_raw_gct, compute_TPM

input_file = snakemake.input[0]
output_file = snakemake.output[0]
tissue_name = snakemake.wildcards.tissue

raw_df = parse_raw_gct(input_file)
median_df = compute_TPM(raw_df)

# Rename the column to the tissue name for clarity in the master CSV file
median_df.rename(columns={"Median_TPM": tissue_name}, inplace=True)

final_df = median_df[[tissue_name]]
final_df.to_csv(output_file)
