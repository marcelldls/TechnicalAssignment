#!/usr/bin/env python3

"""Tests for package_statistics"""

import os
import unittest
from unittest import mock
from urllib.error import HTTPError

from click.testing import CliRunner

from package_statistics.main import cli
from package_statistics.utilities import (
    CfStatistics,
    avail_architectures,
    decompress_cf,
    download_cf,
)


class TestDownloadCF(unittest.TestCase):
    @mock.patch("urllib.request.urlretrieve")
    def test_OSError(self, mock):
        mock.side_effect = OSError()
        with self.assertRaises(Exception):
            download_cf("", "", "")

    @mock.patch("urllib.request.urlretrieve")
    def test_HTTPError(self, mock):
        mock.side_effect = (
            HTTPError(
                "http://example.com",
                500,
                "Internal Error",
                "",
                None,  # type: ignore
            ),
        )
        with self.assertRaises(Exception):
            download_cf("", "", "")


DATA_DIR = "tests/data/"


class TestDecompressCf(unittest.TestCase):
    """
    Test decompression of a contents file
    """

    test_architecture = "ziptest"
    decompressed_file = f"Contents-{test_architecture}"
    result_path = DATA_DIR + decompressed_file

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
expect_count = [x + 1 for x in range(10)][::-1]
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


expected = [
    "all",
    "amd64",
    "arm64",
    "armel",
    "armhf",
    "i386",
    "mips64el",
    "mipsel",
    "ppc64el",
    "s390x",
]


@mock.patch("urllib.request.urlopen", new=lambda file: open(file, "rb"))
class TestAvail(unittest.TestCase):
    """
    Test retrieval of architectures
    """

    def setUp(self):
        self.data_path = DATA_DIR + "debian_mirror.html"

    def test_list(self):
        """Test if file count is correct for the test2 format example"""
        result = avail_architectures(self.data_path)
        self.assertTrue(result == expected)

url =  "http://ftp.uk.debian.org/debian/dists/stable/main/"
expected_archs = (
    f"Available architectures at {url} are:\n"
    "all\n"
    "amd64\n"
    "arm64\n"
    "armel\n"
    "armhf\n"
    "i386\n"
    "mips64el\n"
    "mipsel\n"
    "ppc64el\n"
    "s390x\n"
)


class TestCli(unittest.TestCase):
    """
    Test parsing of the contents file using test2 contents file format
    """

    def test_cli(self):
        """Test cli"""
        cli

    def test_hello_world(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["avail"])
        assert result.exit_code == 0
        assert result.output == expected_archs


if __name__ == "__main__":
    unittest.main()
