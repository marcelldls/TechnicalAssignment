#!/usr/bin/env python3

"""Tests for package_statistics"""

import unittest
import os
from package_statistics import download_cf

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

if __name__ == '__main__':
    unittest.main()
