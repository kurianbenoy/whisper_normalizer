import csv
import unittest
import sys
import os
from indic_normalizer import MalayalamNormalizer

normalizer = MalayalamNormalizer()


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


import unittest

class TestMalayalamNormalization(unittest.TestCase):
    def test_normalization(self):
        # Read the data from the tab separated file
        with open(os.path.join(CURR_DIR, "ml_norm.tsv")) as f:
            data = f.readlines()

        # Create a list of tuples containing the input and normalized strings
        test_data = [(line.split("\t")[0], line.split("\t")[1].strip()) for line in data]

        # Test the normalization function for each input string
        for input_string, normalized_string in test_data:
            self.assertEqual(normalizer(input_string), normalized_string)

if __name__ == "__main__":
    unittest.main()