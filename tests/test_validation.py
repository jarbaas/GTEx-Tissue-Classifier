import unittest
import numpy as np
import pandas as pd
from gtex_tissue_classifier.validation import InputValidation


class TestInputValidation(unittest.TestCase):

    def setUp(self):
        """
        Runs before each test. Creates a minimal valid sample DataFrame and
        reference matrix matching the simulated data format (Gene_0, Gene_1, ...).
        """
        self.valid_df = pd.DataFrame({
            'Gene': ['Gene_0', 'Gene_1', 'Gene_2'],
            'TPM': [1.23, 0.72, 0.87]
        })

        self.reference = pd.DataFrame(
            {'Tissue_0': [50.0, 0.1, 100.0], 'Tissue_1': [10.0, 200.0, 5.0]},
            index=['Gene_0', 'Gene_1', 'Gene_2']
        )

    def _make_validator(self, df=None, ref=None):
        return InputValidation(
            df if df is not None else self.valid_df,
            ref if ref is not None else self.reference
        )

    # ------------------------------------------------------------------
    # check_numeric
    # ------------------------------------------------------------------

    def test_check_numeric_passes_on_valid_data(self):
        """Valid numeric TPM column should not raise."""
        validator = self._make_validator()
        validator.check_numeric()  # no exception

    def test_check_numeric_raises_on_string_tpm(self):
        """TPM column containing strings should raise ValueError."""
        df = self.valid_df.copy()
        df['TPM'] = ['high', 'low', 'medium']
        validator = self._make_validator(df=df)
        with self.assertRaises(ValueError) as ctx:
            validator.check_numeric()
        self.assertIn("numeric", str(ctx.exception))

    def test_check_numeric_raises_on_mixed_tpm(self):
        """TPM column with one string entry (object dtype) should raise ValueError."""
        df = self.valid_df.copy().astype({'TPM': object})
        df.loc[0, 'TPM'] = 'high'
        validator = self._make_validator(df=df)
        with self.assertRaises(ValueError):
            validator.check_numeric()

    # ------------------------------------------------------------------
    # check_positive_domain
    # ------------------------------------------------------------------

    def test_check_positive_domain_passes_on_valid_data(self):
        """All non-negative TPM values should not raise."""
        validator = self._make_validator()
        validator.check_positive_domain()  # no exception

    def test_check_positive_domain_passes_on_zero(self):
        """TPM value of 0.0 is valid and should not raise."""
        df = self.valid_df.copy()
        df['TPM'] = [0.0, 0.0, 0.0]
        validator = self._make_validator(df=df)
        validator.check_positive_domain()  # no exception

    def test_check_positive_domain_raises_on_negative(self):
        """A single negative TPM value should raise ValueError."""
        df = self.valid_df.copy()
        df.loc[1, 'TPM'] = -5.0
        validator = self._make_validator(df=df)
        with self.assertRaises(ValueError) as ctx:
            validator.check_positive_domain()
        self.assertIn("negative", str(ctx.exception))

    def test_check_positive_domain_reports_count(self):
        """Error message should report the number of negative values found."""
        df = self.valid_df.copy()
        df['TPM'] = [-1.0, -2.0, 10.0]
        validator = self._make_validator(df=df)
        with self.assertRaises(ValueError) as ctx:
            validator.check_positive_domain()
        self.assertIn("2", str(ctx.exception))

    # ------------------------------------------------------------------
    # check_missing_values
    # ------------------------------------------------------------------

    def test_check_missing_values_passes_on_valid_data(self):
        """No NaN values should return the DataFrame unchanged."""
        validator = self._make_validator()
        result = validator.check_missing_values()
        self.assertEqual(len(result), 3)

    def test_check_missing_values_drops_nan_tpm(self):
        """Row with NaN in TPM should be dropped and warning emitted."""
        df = self.valid_df.copy()
        df.loc[1, 'TPM'] = np.nan
        validator = self._make_validator(df=df)
        result = validator.check_missing_values()
        self.assertEqual(len(result), 2)

    def test_check_missing_values_drops_none_tpm(self):
        """Row with None in TPM should be treated as NaN and dropped."""
        df = self.valid_df.copy().astype({'TPM': object})
        df.loc[0, 'TPM'] = None
        validator = self._make_validator(df=df)
        result = validator.check_missing_values()
        self.assertEqual(len(result), 2)

    def test_check_missing_values_drops_nan_gene(self):
        """Row with NaN in Gene should be dropped."""
        df = self.valid_df.copy()
        df.loc[2, 'Gene'] = np.nan
        validator = self._make_validator(df=df)
        result = validator.check_missing_values()
        self.assertEqual(len(result), 2)

    def test_check_missing_values_warns_to_stderr(self):
        """A warning should be printed to stderr when rows are dropped."""
        import io
        import sys
        df = self.valid_df.copy()
        df.loc[0, 'TPM'] = np.nan
        validator = self._make_validator(df=df)
        captured = io.StringIO()
        sys.stderr = captured
        try:
            validator.check_missing_values()
        finally:
            sys.stderr = sys.__stderr__
        self.assertIn("Warning", captured.getvalue())

    # ------------------------------------------------------------------
    # check_gene_overlap
    # ------------------------------------------------------------------

    def test_check_gene_overlap_passes_on_full_overlap(self):
        """100% gene overlap should not raise."""
        validator = self._make_validator()
        validator.check_gene_overlap()  # no exception

    def test_check_gene_overlap_raises_on_zero_overlap(self):
        """No matching genes should raise ValueError."""
        df = pd.DataFrame({
            'Gene': ['Gene_99', 'Gene_100'],
            'TPM': [10.0, 20.0]
        })
        validator = self._make_validator(df=df)
        with self.assertRaises(ValueError) as ctx:
            validator.check_gene_overlap()
        self.assertIn("overlap", str(ctx.exception).lower())

    def test_check_gene_overlap_raises_below_threshold(self):
        """Overlap below the 20% default threshold should raise ValueError."""
        # 1 of 6 sample genes matches reference = 16.7% -> below 20% threshold
        df = pd.DataFrame({
            'Gene': ['Gene_0', 'Gene_10', 'Gene_11', 'Gene_12', 'Gene_13', 'Gene_14'],
            'TPM': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        })
        validator = self._make_validator(df=df)
        with self.assertRaises(ValueError) as ctx:
            validator.check_gene_overlap()
        self.assertIn("overlap", str(ctx.exception).lower())

    def test_check_gene_overlap_custom_threshold(self):
        """A custom minimum_threshold should be respected."""
        # 1 of 3 sample genes matches reference = 33%, passes 20% but fails 50%
        df = pd.DataFrame({
            'Gene': ['Gene_0', 'Gene_10', 'Gene_11'],
            'TPM': [1.0, 2.0, 3.0]
        })
        validator = self._make_validator(df=df)
        with self.assertRaises(ValueError):
            validator.check_gene_overlap(minimum_threshold=0.50)

    # ------------------------------------------------------------------
    # run_all_validations
    # ------------------------------------------------------------------

    def test_run_all_validations_passes_on_valid_data(self):
        """A fully valid DataFrame should pass all checks and return a DataFrame."""
        validator = self._make_validator()
        result = validator.run_all_validations()
        self.assertIsInstance(result, pd.DataFrame)

    def test_run_all_validations_stops_at_first_failure(self):
        """Non-numeric TPM should cause run_all_validations to raise before reaching overlap check."""
        df = self.valid_df.copy()
        df['TPM'] = ['high', 'low', 'medium']
        validator = self._make_validator(df=df)
        with self.assertRaises(ValueError) as ctx:
            validator.run_all_validations()
        self.assertIn("numeric", str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
