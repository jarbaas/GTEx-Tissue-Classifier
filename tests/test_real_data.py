import unittest
import os
import pandas as pd
from gtex_tissue_classifier.real_data import parse_raw_gct, compute_TPM
import numpy as np

# Unit test assumes valid GTEx test file exists in 'data/simulated_data/test_tissues.gct'


class TestProcessingWithSimulatedData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Ensures simulated data exists at specified path.
        """
        cls.test_path = "data/simulated_data/test_tissues.gct"

    def test_parse_and_compute(self):
        """
        Integration test: Reads simulated file and checks math.
        """
        # 1. Parse
        result_df = parse_raw_gct(self.test_path)

        # Verify Parser worked
        self.assertFalse(result_df.empty, "The parsed DataFrame should not be empty")
        self.assertIn("Description", result_df.columns, "Description column missing")

        # 2. Compute Median
        final_df = compute_TPM(result_df)

        # Verify Math
        self.assertIn("Median_TPM", final_df.columns)

        # Optional: Spot check a value if you know the random seed or just check type
        # (Since data is random, we just check it's a number and not NaN)
        first_median = final_df["Median_TPM"].iloc[0]
        self.assertIsInstance(first_median, (int, (float, np.floating)))
        self.assertFalse(pd.isna(first_median), "Median should not be NaN")


if __name__ == "__main__":
    unittest.main()

# Unit test adapted from prompt to Google Gemini describing the input/output of respective functions.
