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
        """
        Calculates the overlap in Ensembl IDs between the sample and GTEx reference matrix.
        Raises an error if the overlap ratio falls below minimum_threshold.

        Args:
            minimum_threshold: float, minimum fraction of sample genes that must be
                               present in the reference (default 0.20, i.e. 20%).

        Raises:
            ValueError: if the overlap ratio is below minimum_threshold, reporting
                        the actual overlap percentage and the threshold.
        """
        sample_set = set(self.sample_df['Gene'])
        reference_set = set(self.reference_df.index)

        matching_genes = sample_set.intersection(reference_set)
        overlap_ratio = len(matching_genes) / len(sample_set)

        if overlap_ratio < minimum_threshold:
            raise ValueError(
                f"Insufficient gene overlap with GTEx reference: "
                f"{overlap_ratio:.1%} of sample genes matched "
                f"(minimum required: {minimum_threshold:.1%}). "
                f"Check that Gene column contains valid Ensembl IDs."
            )

    def run_all_validations(self):
        """
        Execute all checks in sequence.
        Execution stops at the first exception raised by a failing check.

        Returns:
            pd.DataFrame: cleaned sample DataFrame (NaN rows removed if any).
        """
        self.check_numeric()
        self.check_positive_domain()
        self.check_missing_values()
        self.check_gene_overlap()
        return self.sample_df