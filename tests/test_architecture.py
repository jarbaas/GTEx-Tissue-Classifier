import unittest
import os
from gtex_tissue_classifier.architecture import read_file_data, PROJECT_ROOT
class TestReadFileData(unittest.TestCase):
    """Class to test the function read_file_data."""

    def setUp(self):
        """Create a temporary file for testing happy path."""
        self.test_filename = 'temp_test_list.txt'
        self.absolute_test_path = os.path.join(PROJECT_ROOT, self.test_filename)
        with open(self.absolute_test_path, 'w') as f:
            f.write("Adipose_Subcutaneous\n")
            f.write("Liver\n")
            f.write("  \n")
            f.write("Brain_Cortex")

    def tearDown(self):
        """Clean up the temporary file after tests run."""
        if os.path.exists(self.absolute_test_path):
            os.remove(self.absolute_test_path)

    def test_read_file_success(self):
        """Test case: Successfully reading and stripping valid data."""
        expected = ["Adipose_Subcutaneous", "Liver", "Brain_Cortex"]
        result = read_file_data(self.test_filename)
        self.assertEqual(result, expected, "The function should strip whitespace and skip empty lines.")

    def test_file_not_found(self):
        """Test case: Handling a missing file branch."""
        with self.assertRaises(FileNotFoundError):
            read_file_data("non_existent_file.txt")

if __name__ == '__main__':
    unittest.main()