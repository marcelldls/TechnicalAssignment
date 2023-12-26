#!/usr/bin/env python3

"""
A python command line tool that takes architecture (amd64, arm64, etc.) as an argument and outputs
the statistics of the top 10 packages (from Debian mirror:
http://ftp.uk.debian.org/debian/dists/stable/main/) that have the most files associated with them.
"""

import argparse
import os
import urllib.request
import urllib.error
import gzip
import shutil
import tempfile


def download_cf(architecture, debian_mirror, dir):
    """Takes architecture (string) and downloads associated contents file from the debian mirror"""

    contents_file = 'Contents-' + architecture + '.gz'
    path = os.path.join(dir, contents_file)
    remote_url = debian_mirror + contents_file

    try:  # Test connection
        print('Attempt to connect to Debian mirror...')
        urllib.request.urlopen(debian_mirror, timeout=1.0)
        print('Connection to Debian mirror successful!')
    except:
        raise Exception('Unable to connect to Debian mirror') from None   # PEP 409

    try:   # Download file and save locally
        print('Retrieving file: ' + contents_file)
        urllib.request.urlretrieve(remote_url, path)
        print('Contents file sucessfully retrieved!')
    except:
        raise Exception('Failed to locate contents file for '+ architecture) from None

def decompress_cf(architecture, dir):
    """Takes architecture (string) and decompresses associated contents file"""

    print('Decompressing contents file')
    contents_file = 'Contents-' + architecture
    compressed_file = os.path.join(dir, contents_file + '.gz')
    decompressed_file = os.path.join(dir, contents_file)

    # Decompress file
    with gzip.open(compressed_file, 'rb') as f_in:
        with open(decompressed_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Clean up by deleting downloaded compressed file
    os.remove(compressed_file)
    print('Contents file decompressed')


class CfStatistics:
    """Contains methods to process an architectures contents file"""

    def __init__(self, architecture, dir):
        self.package_dict = {}     # Dictionary has O(1) search vs list O(n)
        self.package_names = []
        self.file_count = []
        self.architecture = architecture
        self.dir = dir
        self.__tally()
        self.__sort()

    def __tally(self):
        # load file
        file_name = 'Contents-' + self.architecture
        path = os.path.join(self.dir, file_name)
        print("Parsing contents file")
        with open(path, 'rt', errors='ignore') as file:

            # Search For header
            start_line = 0
            for i in range(100):
                line = file.readline()
                if "".join(line.split()) == "FILELOCATION":
                    start_line = i
            print("Starting scan from line" + ' ' + str(start_line))

        with open(path, 'rt', errors='ignore') as file:

            # Scan each line
            for num, line in enumerate(file):

                # Skip line if before or is header
                if num <= start_line-1:
                    continue

                # Extract name as string
                line = line.strip('\n')
                name_idx = line.rfind('/')      # Find index where name starts
                line_name = line[name_idx+1:]   # Slice out name

                # Populate dictionary with unique names and occurances
                if line_name not in self.package_dict:
                    self.package_dict[line_name] = 1     # unique key
                else:
                    self.package_dict[line_name] += 1    # existing key

    def __sort(self):   # Assumes more than 10 unique packages exist in repo
        sorted_dict = sorted(self.package_dict.items(), key=lambda item: item[1]) # list of tuples
        self.file_count = [sorted_dict[-(i+1)][1] for i in range(10)]     # Extract top 10 values
        self.package_names = [sorted_dict[-(i+1)][0] for i in range(10)]  # Extract top 10 keys

    def print_top10(self):
        """Prints a numerated list of the top 10 ranked packages for file count"""
        print('The top 10 packages with the highest file counts are:')
        for i in range(len(self.package_names)):
            print(str(i+1), end='. ')
            print(self.package_names[i], end='  ')
            print(self.file_count[i])

if __name__ == "__main__":

    DEB_MIRROR = "http://ftp.uk.debian.org/debian/dists/stable/main/"

    # Process arguments
    parser = argparse.ArgumentParser(prog='package_statistics.py')
    parser.add_argument(
        "architecture",
        help="Desired architecture (amd64, arm64, etc.)",
        )
    parser.add_argument(
        "--debian_mirror",
        metavar='',
        default=DEB_MIRROR,
        help=f"Desired Debian Mirror. Default: {DEB_MIRROR}",
        )
    args = parser.parse_args()
    print("Process package statistics for:", args.architecture)

    with tempfile.TemporaryDirectory() as tmpdirname:

        # Aquire contents file in working directory
        download_cf(args.architecture, args.debian_mirror, tmpdirname)
        decompress_cf(args.architecture, tmpdirname)

        # Process data
        archStats = CfStatistics(args.architecture, tmpdirname)

        # Return results
        archStats.print_top10()
