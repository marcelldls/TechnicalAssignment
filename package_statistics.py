#!/usr/bin/env python3

"""
A python command line tool that takes architecture (amd64, arm64, etc.) as an argument and outputs
the statistics of the top 10 packages (from Debian mirror:
http://ftp.uk.debian.org/debian/dists/stable/main/) that have the most files associated with them.
"""

import sys
import urllib.request
import urllib.error

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

if __name__ == "__main__":
    print("Initialising")
    download_cf(sys.argv[1])
    print("Complete")
