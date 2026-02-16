import unittest
import os
import pandas as pd
import numpy as np
from gtex_tissue_classifier.architecture import load_input, validate_normalization, read_file_data

class TestArchitecture(unittest.TestCase):

    def setUp(self):
        """
        Runs before EACH test. Creates temporary files for testing.
        """
        # 1. Setup paths
        self.valid_csv = "test_valid_input.csv"
        self.missing_col_csv = "test_missing_cols.csv"
        self.bad_format_csv = "test_bad_format.txt"
        self.text_list_file = "test_list_data.txt"

        # 2. Create a VALID input CSV
        df_valid = pd.DataFrame({
            'Gene': ['ENSG01', 'ENSG02', 'ENSG03'],
            'TPM': [10.5, 0.0, 100.2]
        })
        df_valid.to_csv(self.valid_csv, index=False)

        # 3. Create an INVALID CSV (Missing 'TPM' column)
        df_missing = pd.DataFrame({
            'Gene': ['ENSG01', 'ENSG02'],
            'Count': [10, 20] # Wrong column name
        })
        df_missing.to_csv(self.missing_col_csv, index=False)
        
        # 4. Create a Text File for read_file_data
        with open(self.text_list_file, 'w') as f:
            f.write("Line 1\nLine 2\nLine 3")

    def tearDown(self):
        """
        Runs after EACH test. Cleans up the temporary files.
        """
        for f in [self.valid_csv, self.missing_col_csv, self.bad_format_csv, self.text_list_file]:
            if os.path.exists(f):
                os.remove(f)

    # ==========================================
    # TEST 1: load_input
    # ==========================================
    def test_load_input_success(self):
        """Should successfully load a dataframe with Gene and TPM columns."""
        df = load_input(self.valid_csv)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertIn('Gene', df.columns)
        self.assertIn('TPM', df.columns)

    def test_load_input_file_not_found(self):
        """Should raise FileNotFoundError if path does not exist."""
        with self.assertRaises(FileNotFoundError):
            load_input("non_existent_ghost_file.csv")

    def test_load_input_missing_columns(self):
        """Should raise ValueError if 'Gene' or 'TPM' columns are missing."""
        with self.assertRaises(ValueError) as context:
            load_input(self.missing_col_csv)
        self.assertIn("missing required columns", str(context.exception))

    # ==========================================
    # TEST 2: validate_normalization
    # ==========================================
    def test_validate_normalization_success(self):
        """Should return True (or pass) for valid non-negative floats."""
        # Create a clean DF
        df = pd.DataFrame({'Gene': ['A', 'B'], 'TPM': [10.0, 0.5]})
        
        # Assuming function returns True on success or simply doesn't raise
        try:
            result = validate_normalization(df)
            # If your function returns the DF, check that too
            if result is not None and not isinstance(result, bool):
                self.assertIsInstance(result, pd.DataFrame)
        except ValueError:
            self.fail("validate_normalization raised ValueError on valid data!")

    def test_validate_normalization_negative_values(self):
        """Should raise ValueError for negative TPMs (biologically impossible)."""
        df = pd.DataFrame({'Gene': ['A', 'B'], 'TPM': [10.0, -5.0]})
        
        with self.assertRaises(ValueError):
            validate_normalization(df)

    def test_validate_normalization_non_numeric(self):
        """Should raise Error if TPM column contains strings."""
        df = pd.DataFrame({'Gene': ['A', 'B'], 'TPM': [10.0, "High"]})
        
        with self.assertRaises(Exception): # ValueError or TypeError
            validate_normalization(df)

    # ==========================================
    # TEST 3: read_file_data
    # ==========================================
    def test_read_file_data_content(self):
        """Should correctly read lines into a list."""
        result_list = read_file_data(self.text_list_file)
        
        self.assertIsInstance(result_list, list)
        self.assertEqual(len(result_list), 3)
        self.assertEqual(result_list[0].strip(), "Line 1")
        self.assertEqual(result_list[2].strip(), "Line 3")

    def test_read_file_data_missing(self):
        """Should handle missing files appropriately (raise error)."""
        with self.assertRaises(FileNotFoundError):
            read_file_data("ghost_text_file.txt")

if __name__ == '__main__':
    unittest.main()

# Unit test adapted from prompt to Google Gemini describing the input/output of respective functions. 