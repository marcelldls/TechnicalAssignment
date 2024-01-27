"""
A python command line tool that takes architecture (amd64, arm64, etc.) as an 
argument and outputs the statistics of the top 10 packages from a Debian 
mirror that have the most files associated with them.
"""

import argparse
import logging
import tempfile

from package_statistics.utilities import (
    CfStatistics,
    decompress_cf,
    download_cf,
)


def cli():
    DEB_MIRROR = "http://ftp.uk.debian.org/debian/dists/stable/main/"

    # Process arguments
    parser = argparse.ArgumentParser(
        prog="package_statistics", description=__doc__
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
        help=f"desired Debian Mirror (Default: {DEB_MIRROR})",
        default=DEB_MIRROR,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format="%(message)s")

    print(
        f"Processing package statistics for '{args.arch}'",
        f"from {args.debian_mirror}",
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Aquire contents file in working directory
        download_cf(args.arch, args.debian_mirror, tmpdirname)
        decompress_cf(args.arch, tmpdirname)

        # Process data
        archStats = CfStatistics(args.arch, tmpdirname)

        # Return results
        archStats.print_top10()


if __name__ == "__main__":
    cli()
