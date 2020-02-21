#===============================================================================
# download_example_bw.py
#===============================================================================

# Imports ======================================================================

import os.path
import subprocess

from argparse import ArgumentParser
from shutil import copyfileobj
from urllib.request import urlopen




# Constants ====================================================================

EXAMPLE_BIGWIG_URL = 'http://genome.ucsc.edu/goldenPath/help/examples/bigWigExample.bw'
EXAMPLE_BIGWIG_PATH = os.path.join(os.path.dirname(__file__), 'bigWigExample.bw')




# Functions ====================================================================

def download_example_bigwig(
    example_bigwig_path=EXAMPLE_BIGWIG_PATH
):
    print(
        'Downloading example bigwig file to '
        f'{example_bigwig_path}'
    )
    with urlopen(EXAMPLE_BIGWIG_URL) as (
        response
    ), open(example_bigwig_path, 'wb') as (
        f
    ):
        copyfileobj(response, f)


def parse_arguments():
    parser = ArgumentParser(description='download an example BigWig file')
    parser.add_argument(
        '--dest',
        metavar='<path/to/dest.bw>',
        default=EXAMPLE_BIGWIG_PATH,
        help=f'destination for the example BigWig file [{EXAMPLE_BIGWIG_PATH}]'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    download_example_bigwig(args.dest)
