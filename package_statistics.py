#!/usr/bin/env python3

"""
A python command line tool that takes architecture (amd64, arm64, etc.) as an argument and outputs
the statistics of the top 10 packages (from Debian mirror:
http://ftp.uk.debian.org/debian/dists/stable/main/) that have the most files associated with them.
"""

import sys
import os
import urllib.request
import urllib.error
import gzip
import shutil

def read_args(args):
    """Process user arguments from command line - Exit if unexpected number"""
    assert (len(args) == 2), "Expect architecture (amd64, arm64, etc.) as only argument"
    return args[1]

def download_cf(architecture):
    """Takes architecture (string) and downloads associated contents file from the debian mirror"""

    debian_mirror = 'http://ftp.uk.debian.org/debian/dists/stable/main/'
    contents_file = 'Contents-' + architecture + '.gz'
    remote_url = debian_mirror + contents_file

    try:  # Test connection
        print('Attempt to connect to Debian mirror...')
        urllib.request.urlopen(debian_mirror, timeout=1.0)
        print('Connection to Debian mirror successful!')
    except:
        raise Exception('Unable to connect to Debian mirror') from None   # PEP 409

    try:   # Download file and save locally
        print('Retriving file: ' + contents_file)
        urllib.request.urlretrieve(remote_url, contents_file)
        print('Contents file sucessfully retrieved!')
    except:
        raise Exception('Failed to locate contents file for '+ architecture) from None

def decompress_cf(architecture):
    """Takes architecture (string) and decompresses associated contents file"""

    print('Decompressing contents file')
    contents_file = 'Contents-' + architecture
    compressed_file = contents_file + '.gz'

    # Decompress file
    with gzip.open(compressed_file, 'rb') as f_in:
        with open(contents_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Clean up by deleting compressed file
    os.remove(compressed_file)
    print('Contents file decompressed')

def cleanup_cf(architecture):
    """Takes architecture (string) and deletes associated contents file"""

    print('Cleaning up working directory')
    contents_file = 'Contents-' + architecture
    os.remove(contents_file)
    print('Clean up complete')

if __name__ == "__main__":
    print("Initialising")

    # Process command line arguments
    ARCH = read_args(sys.argv)

    # Aquire contents file in working directory
    download_cf(ARCH)
    decompress_cf(ARCH)

    # Exit process
    cleanup_cf(ARCH)
    print("Complete")
