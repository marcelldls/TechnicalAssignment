"""
A python command line tool that takes architecture (amd64, arm64, etc.) as an 
argument and outputs the statistics of the top 10 packages from a Debian 
mirror that have the most files associated with them.
"""

import argparse
import gzip
import logging
import os
import shutil
import tempfile
import urllib.error
import urllib.request


def download_cf(
    architecture: str, debian_mirror: str, working_dir: str
) -> None:
    """Download architecture contents file from the debian mirror"""

    contents_file = "Contents-" + architecture + ".gz"
    path = os.path.join(working_dir, contents_file)
    remote_url = debian_mirror + contents_file

    try:  # Download file and save locally
        logging.info("Retrieving file: " + contents_file)
        urllib.request.urlretrieve(remote_url, path)
        logging.info("Contents file sucessfully retrieved!")
    except urllib.error.HTTPError as e:
        raise Exception(
            f"{e}. Is '{architecture}' a valid architecture?"
        ) from e
    except OSError as e:
        raise Exception(f"{e}: Is your internet connection active?") from e


def decompress_cf(architecture: str, dir: str) -> None:
    """Decompresses an architecture contents file"""

    contents_file = "Contents-" + architecture
    compressed_file = os.path.join(dir, contents_file + ".gz")
    decompressed_file = os.path.join(dir, contents_file)

    # Decompress file
    logging.info("Decompressing contents file")
    with gzip.open(compressed_file, "rb") as f_in:
        with open(decompressed_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    logging.info("Contents file decompressed")


class CfStatistics:
    """Process statistics of an architecture contents file"""

    def __init__(self, architecture, dir):
        self.package_dict = {}  # Dictionary has O(1) search vs list O(n)
        self.package_names = []
        self.file_count = []
        self.architecture = architecture
        self.dir = dir
        self.__tally()
        self.__sort()

    def __tally(self):
        # load file
        file_name = "Contents-" + self.architecture
        path = os.path.join(self.dir, file_name)
        logging.info("Parsing contents file")
        with open(path, "rt", errors="ignore") as file:
            # Search For header
            start_line = 0
            for i in range(100):
                line = file.readline()
                if "".join(line.split()) == "FILELOCATION":
                    start_line = i
            logging.info("Starting scan from line" + " " + str(start_line))

        with open(path, "rt", errors="ignore") as file:
            # Scan each line
            for num, raw_line in enumerate(file):
                # Skip line if before or is header
                if num <= start_line - 1:
                    continue

                # Extract name as string
                line = raw_line.strip("\n")
                name_idx = line.rfind("/")  # Find index where name starts
                line_name = line[name_idx + 1 :]  # Slice out name

                # Populate dictionary with unique names and occurances
                if line_name not in self.package_dict:
                    self.package_dict[line_name] = 1  # unique key
                else:
                    self.package_dict[line_name] += 1  # existing key

    def __sort(self):
        sorted_dict = sorted(
            self.package_dict.items(), key=lambda item: item[1]
        )  # list of tuples
        self.file_count = [
            sorted_dict[-(i + 1)][1] for i in range(len(sorted_dict))
        ]
        self.package_names = [
            sorted_dict[-(i + 1)][0] for i in range(len(sorted_dict))
        ]

    def print_top10(self):
        print("The top 10 packages with the highest file counts are:")
        for i in range(10):
            try:
                print(f"{i+1}. {self.package_names[i]}  {self.file_count[i]}")
            except IndexError:  # Handle less than 10 unique packages
                print(f"{i+1}.")


def main():
    DEB_MIRROR = "http://ftp.uk.debian.org/debian/dists/stable/main/"

    # Process arguments
    parser = argparse.ArgumentParser(
        prog="package_statistics.py", description=__doc__
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="verbose output",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        default=logging.WARNING,
    )
    parser.add_argument(
        "arch",
        metavar="architecture",
        help="desired architecture (amd64, arm64, etc.)",
    )
    parser.add_argument(
        "--debian_mirror",
        metavar="",
        default=DEB_MIRROR,
        help=f"desired Debian Mirror (Default: {DEB_MIRROR})",
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format="%(message)s")
    print(f"Processing package statistics for {args.arch}...")

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Aquire contents file in working directory
        download_cf(args.arch, args.debian_mirror, tmpdirname)
        decompress_cf(args.arch, tmpdirname)

        # Process data
        archStats = CfStatistics(args.arch, tmpdirname)

        # Return results
        archStats.print_top10()


if __name__ == "__main__":
    main()
