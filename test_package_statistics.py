#!/usr/bin/env python3

"""Tests for package_statistics"""

import unittest
import os
from package_statistics import read_args, download_cf, decompress_cf, cleanup_cf

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
    Only using amd64 otherwise test duration is long (each architecture ~10mb files)
    """
    test_architecture = 'amd64'
    test_file = 'Contents-' + test_architecture + '.gz'

    def setUp(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_download(self):
        """Test downloading of contents file"""
        download_cf(self.test_architecture)
        self.assertTrue(os.path.exists(self.test_file))
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

class TestDecompressCf(unittest.TestCase):
    """
    Test decompression of contents file
    """
    test_architecture = 'amd64'
    decompressed_file = 'Contents-' + test_architecture

    def setUp(self):
        if os.path.exists(self.decompressed_file):
            os.remove(self.decompressed_file)

    def test_decompress(self):
        """Test decompression of contents file"""
        open(self.decompressed_file, 'w').close()    # Create empty file
        os.system('gzip ' + self.decompressed_file)
        decompress_cf(self.test_architecture)
        self.assertTrue(os.path.exists(self.decompressed_file))
        if os.path.exists(self.decompressed_file):
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

if __name__ == '__main__':
    unittest.main()
