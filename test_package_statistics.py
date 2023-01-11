#!/usr/bin/env python3

"""Tests for package_statistics"""

import unittest
import os
from package_statistics import download_cf, decompress_cf, cleanup_cf

class TestDownloadCf(unittest.TestCase):
    """
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
    Only using amd64 otherwise test duration is long (each architecture ~10mb files)
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
    Only using amd64 otherwise test duration is long (each architecture ~10mb files)
    """
    test_architecture = 'amd64'
    target_file = 'Contents-' + test_architecture

    def test_cleanup(self):
        """Test cleanup of contents file"""
        open(self.target_file, 'w').close()    # Create empty file
        cleanup_cf(self.test_architecture)
        self.assertFalse(os.path.exists(self.target_file))

if __name__ == '__main__':
    unittest.main()
