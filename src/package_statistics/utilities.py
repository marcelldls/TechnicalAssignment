import gzip
import logging
import os
import re
import shutil
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
            for num, line in enumerate(file):
                if "".join(line.split()) == "FILELOCATION":
                    start_line = num + 1
            logging.info(f"Starting scan from line {start_line}")

        with open(path, "rt", errors="ignore") as file:
            # Scan each line
            for num, raw_line in enumerate(file):
                # Skip line if before or is header
                if num < start_line:
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


def avail_architectures(debian_mirror: str) -> list[str]:

    with urllib.request.urlopen(debian_mirror) as response:
        raw = response.read().decode("utf-8")

    filter = '<*href="binary-(.*)\/"'  # https://regex101.com/r/NqS4yK/1
    urllist = re.findall(filter, raw)

    return urllist