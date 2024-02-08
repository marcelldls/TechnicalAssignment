#!/usr/bin/env python3

"""Tests for package_statistics"""

import unittest
from unittest import mock

from click.testing import CliRunner

from package_statistics.main import cli

DATA_DIR = "tests/data/"


arch_data_path = DATA_DIR + "debian_mirror.html"
expected_archs = (
    f"Available architectures at {arch_data_path} are:\n"
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

expected_list = (
    "Processing package statistics for 'ziptest' from http://ftp.uk.debian.org/debian/dists/stable/main/\n"
    "The top 10 packages with the highest file counts are:\n"
    "1.espeak-ng-data-udeb          488\n"
    "2.brltty-udeb                  430\n"
    "3.espeak-data-udeb             275\n"
    "4.busybox-udeb                 114\n"
    "5.libgdk-pixbuf-2.0-0-udeb     111\n"
    "6.libglib2.0-udeb              110\n"
    "7.at-spi2-core-udeb            109\n"
    "8.libasound2-udeb              80\n"
    "9.partman-base                 65\n"
    "10.fontconfig-udeb              64\n"
)

class TestCli(unittest.TestCase):
    """
    Test parsing of the contents file using test2 contents file format
    """

    def setUp(self):
        self.runner = CliRunner()

    @mock.patch("urllib.request.urlopen", new=lambda file: open(file, "rb"))
    def test_avail(self):
        result = self.runner.invoke(cli, ["-m", arch_data_path, "avail"])
        assert result.exit_code == 0
        assert result.output == expected_archs

    @mock.patch("urllib.request.urlretrieve", new=lambda *args: None)
    @mock.patch('tempfile.TemporaryDirectory')
    def test_list(self, mock):
        mock.return_value.__enter__.return_value = DATA_DIR
        result = self.runner.invoke(cli, ["list", "ziptest"])
        assert result.exit_code == 0
        assert result.output == expected_list


if __name__ == "__main__":
    unittest.main()
