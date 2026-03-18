import pandas as pd

input_files = snakemake.input
output_file = snakemake.output[0]

master_df = pd.read_csv(input_files[0], index_col="Name")

for file in input_files[1:]:
    df = pd.read_csv(file, index_col="Name")
    master_df = master_df.join(df, how="outer")

master_df.to_csv(output_file)
