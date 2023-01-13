#!/usr/bin/env python3

"""Tests for package_statistics"""

import unittest
import os
import gzip
import shutil
import sys
sys.path.append('../')
from package_statistics import read_args, download_cf, decompress_cf, cleanup_cf, CfStatistics

class TestReadArgs(unittest.TestCase):
    """
    Test processing of user arguments
    """
    test_architecture = 'amd64'
    test_file = 'Contents-' + test_architecture + '.gz'

    def test_two(self):
        """Test processing of two arguments"""
        sys_args1 = ['./package_statistics.py', 'amd64']
        args_1 = read_args(sys_args1)
        self.assertTrue(args_1 == 'amd64')

    def test_few(self):
        """Test processing of too few arguments"""
        sys_args2 = ['./package_statistics.py']
        result_few = False
        try:
            read_args(sys_args2)
        except AssertionError:
            result_few = True
        self.assertTrue(result_few)

    def test_many(self):
        """Test processing of too many arguments"""
        sys_args3 = ['./package_statistics.py', 'amd64', 'arm64']
        result_many = False
        try:
            read_args(sys_args3)
        except AssertionError:
            result_many = True
        self.assertTrue(result_many)

class TestDownloadCf(unittest.TestCase):
    """
    Test downloading of contents file
    Only using amd64 otherwise test duration is long
    """
    test_architecture = 'amd64'
    test_file = 'Contents-' + test_architecture + '.gz'

    def setUp(self): # Remove any preexisting contents file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_download(self):
        """Test downloading of contents file"""
        download_cf(self.test_architecture)
        self.assertTrue(os.path.exists(self.test_file))
        if os.path.exists(self.test_file):   # Clean up
            os.remove(self.test_file)

class TestDecompressCf(unittest.TestCase):
    """
    Test decompression of contents file
    """
    test_architecture = 'amd64'
    decompressed_file = 'Contents-' + test_architecture

    def setUp(self): # Remove any preexisting contents file
        if os.path.exists(self.decompressed_file):
            os.remove(self.decompressed_file)

    def test_decompress(self):
        """Test decompression of contents file"""
        open(self.decompressed_file, 'w').close()    # Create empty file

        # Compress file
        with open(self.decompressed_file, 'rb') as f_in:
            with gzip.open(self.decompressed_file+'.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(self.decompressed_file) # Clean up by deleting uncompressed file

        decompress_cf(self.test_architecture)
        self.assertTrue(os.path.exists(self.decompressed_file))
        if os.path.exists(self.decompressed_file):  # Clean up
            os.remove(self.decompressed_file)

class TestCleanup(unittest.TestCase):
    """
    Test cleaning up of contents file
    """
    test_architecture = 'amd64'
    target_file = 'Contents-' + test_architecture

    def test_cleanup(self):
        """Test cleaning up of contents file"""
        open(self.target_file, 'w').close()    # Create empty file
        cleanup_cf(self.test_architecture)
        self.assertFalse(os.path.exists(self.target_file))

class TestCf1Statistics(unittest.TestCase):
    """
    Test parsing of the contents file using test1 contents file format
    """

    def setUp(self):
        self.expect_count = [17, 14, 12, 10, 8, 7, 6, 5, 4, 3]  # Manually counted
        self.expect_names = ['package_'+str(x+1) for x in range(10)] # Expected package rank
        self.test1_stats = CfStatistics('test1')

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
        self.expect_count = [17, 14, 12, 10, 8, 7, 6, 5, 4, 3]  # Manually counted
        self.expect_names = ['package_'+str(x+1) for x in range(10)] # Expected package rank
        self.test2_stats = CfStatistics('test2')

    def test2_count(self):
        """Test if file count is correct for the test2 format example"""
        self.assertTrue(self.test2_stats.file_count == self.expect_count)

    def test2_rank(self):
        """Test if rank is correct for the test2 format example"""
        self.assertTrue(self.test2_stats.package_names == self.expect_names)

if __name__ == '__main__':
    unittest.main()
