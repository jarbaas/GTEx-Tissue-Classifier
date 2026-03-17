import sys
import pandas as pd

class InputValidation:
    """
    Validates the integrity of GTEx-Tissue-Classifier input files, RNA-seq sample and GTEx reference matrix.
    """
    def __init__(self, sample_df, reference_df):
        self.sample_df = sample_df
        self.reference_df = reference_df

    def check_numeric(self):
        """
        Checks that the TPM column contains only numeric values.

        Raises:
            ValueError: if TPM column dtype is not numeric.
        """
        if not pd.api.types.is_numeric_dtype(self.sample_df['TPM']):
            raise ValueError("TPM column must contain numeric values, not strings or characters.")

    def check_positive_domain(self):
        """
        Checks that all TPM values are non-negative (>= 0).

        Raises:
            ValueError: if any TPM value is negative, reporting the count.
        """
        n = (self.sample_df['TPM'] < 0).sum()
        if n > 0:
            raise ValueError(f"TPM values cannot be negative. Found {n} negative values.")

    def check_missing_values(self):
        """
        Checks for NaN or None in the TPM and Gene columns.
        Drops affected rows and prints a warning to stderr reporting how many were removed.

        Returns:
            pd.DataFrame: cleaned DataFrame with NaN rows removed.
        """
        nan_mask = self.sample_df['TPM'].isna() | self.sample_df['Gene'].isna()
        n = nan_mask.sum()
        if n > 0:
            print(
                f"Warning: {n} row(s) with NaN/None values were removed from the input.",
                file=sys.stderr,
            )
            self.sample_df = self.sample_df[~nan_mask].reset_index(drop=True)
        return self.sample_df

    def check_gene_overlap(self, minimum_threshold=0.20):
        sample_genes = sample_df['Gene'].tolist()
        reference_genes = reference_df.index.tolist()
        sample_set = set(sample_genes)
        reference_set = set(reference_genes)

        # Calculate intersection of the two sets
        matching_genes = sample_set.intersection(reference_set)

        # Calculate overlap of the two sets
        overlap_ratio = length(matching_genes) / length(sample_set)
        
        # If overlap_ratio < minimum_threshold:
            # Raise custom error like InsufficientOverlap

    def run_all_validations(self):
        """
        Execute all checks in sequence.
        """
        # check_numeric_values()
        # check_positive_domain()
        # check_missing_values()
        # check_gene_overlap()
        # Return True if all pass, otherwise execution stops when exceptions are reached.