#!/usr/bin/env python3

"""Tests for package_statistics"""

import os
import unittest

from package_statistics import (
    CfStatistics,
    decompress_cf,
)

DATA_DIR = "tests/data/"

class TestDecompressCf(unittest.TestCase):
    """
    Test decompression of contents file
    """

    test_architecture = "ziptest"
    decompressed_file = f"Contents-{test_architecture}"
    result_path = DATA_DIR+decompressed_file

    def setUp(self):  # Remove any preexisting contents file
        if os.path.exists(self.decompressed_file):
            os.remove(self.decompressed_file)

    def test_decompress(self):
        """Test decompression of contents file"""
        decompress_cf(self.test_architecture, "tests/data/")
        self.assertTrue(os.path.exists(self.result_path))

    def tearDown(self):
        if os.path.exists(self.result_path):
            os.remove(self.result_path)


# Manually counted
expect_count = [x+1 for x in range(10)][::-1]
expect_names = ["package_" + str(x + 1) for x in range(10)][::-1]


class TestCf1Statistics(unittest.TestCase):
    """
    Test parsing of the contents file using test1 contents file format
    """

    def setUp(self):
        self.expect_count = expect_count
        self.expect_names = expect_names
        self.test1_stats = CfStatistics("test1", DATA_DIR)

    def test1_count(self):
        """Test if file count is correct for the test1 format example"""
        self.assertTrue(self.test1_stats.file_count == self.expect_count)

    def test1_rank(self):
        """Test if rank is correct for the test1 format example"""
        self.assertTrue(self.test1_stats.package_names == self.expect_names)


class TestCf2Statistics(unittest.TestCase):
    """
    Test parsing of the contents file using test2 contents file format
    """

    def setUp(self):
        self.expect_count = expect_count
        self.expect_names = expect_names
        self.test2_stats = CfStatistics("test2", DATA_DIR)

    def test2_count(self):
        """Test if file count is correct for the test2 format example"""
        self.assertTrue(self.test2_stats.file_count == self.expect_count)

    def test2_rank(self):
        """Test if rank is correct for the test2 format example"""
        self.assertTrue(self.test2_stats.package_names == self.expect_names)


if __name__ == "__main__":
    unittest.main()
