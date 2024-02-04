import logging
import tempfile

import click

from package_statistics.utilities import (
    CfStatistics,
    avail_architectures,
    decompress_cf,
    download_cf,
)

DEB_MIRROR = "http://ftp.uk.debian.org/debian/dists/stable/main/"

@click.group()
@click.option('-v', '--verbose', is_flag=True)
@click.option('-m', '--debian_mirror', 'mirror', default=DEB_MIRROR)
@click.pass_context
def cli(ctx, verbose, mirror):
    """
    A python command line tool that takes architecture (amd64, arm64, etc.) as
    an argument and outputs the statistics of the top 10 packages from a Debian
    mirror that have the most files associated with them.
    """
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format="%(message)s")
    ctx.obj = {
        'mirror':mirror,
        }


@cli.command()
@click.argument('arch',  metavar='ARCHITECTURE', required=1)
@click.pass_context
def list(ctx, arch):
    """Show statistics for a given architecture"""
    mirror = ctx.parent.obj['mirror']

    print(
        f"Processing package statistics for '{arch}'",
        f"from {mirror}",
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Aquire contents file in working directory
        download_cf(arch, mirror, tmpdirname)
        decompress_cf(arch, tmpdirname)

        # Process data
        archStats = CfStatistics(arch, tmpdirname)

        # Return results
        archStats.print_top10()


@cli.command()
@click.pass_context
def avail(ctx):
    """fetch and show available architectures"""
    mirror = ctx.parent.obj['mirror']
    arch_list = avail_architectures(mirror)
    click.echo(f"Available architectures at {mirror} are:")
    for arch in arch_list:
        click.echo(arch)


if __name__ == "__main__":
    cli()
