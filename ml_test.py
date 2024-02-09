import unittest
import os
from whisper_normalizer.indic_normalizer import MalayalamNormalizer

normalizer = MalayalamNormalizer()

CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


import unittest

class TestNormalizer(unittest.TestCase):
    def setUp(self):
        # Read input and output data from ml_norm.tsv
        self.test_data = []
        with open(os.path.join(CURR_DIR, "ml_norm.tsv")) as file:
            for line in file:
                input_data, expected_output = line.strip().split('\t')
                self.test_data.append((input_data, expected_output))

    def test_normalizer(self):
        passes = 0
        failures = 0
        failure_list = []
        
        for input_data, expected_output in self.test_data:
            # Apply your normalizer to the input data
            result = normalizer(input_data)
            
            # Compare the result with the expected output
            if result == expected_output:
                passes += 1
            else:
                failures += 1
                failure_list.append((input_data, expected_output, result))
        
        # Print the list of failures and the number of passes
        print("Passes:", passes)
        print("Failures:", failures)
        for failure in failure_list:
            print("Input:", failure[0])
            print("Expected Output:", failure[1])
            print("Actual Output:", failure[2])
            print()  # Add a newline for clarity
    
if __name__ == '__main__':
    unittest.main()
