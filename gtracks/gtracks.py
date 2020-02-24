#===============================================================================
# gtracks.py
#===============================================================================

"""Plot BigWig signal tracks and gene annotations in a genomic region"""




# Imports ======================================================================

import argparse
import gzip
import os
import os.path
import re
import subprocess
import seaborn as sns
import tempfile




# Constants ====================================================================

BIGWIG_CONFIG_FORMAT = """
[{title}]
file={file}
title = {title}
height = 2
color = {color}
min_value = 0
max_value = {max}
file_type = bigwig
"""

SPACER = """

[spacer]

"""

GENES_CONFIG_FORMAT = """
[genes]
file = {}
title = genes
fontsize = 10
height = {}
gene rows = {}
"""

X_AXIS_CONFIG = """
[x-axis]
"""

VLINES_CONFIG_FORMAT = """
[vlines]
file = {}
type = vlines
"""

COLOR_PALETTE = os.environ.get(
    'GTRACKS_COLOR_PALETTE',
    ','.join(sns.color_palette().as_hex())
).split(',')
GENES_PATH = os.environ.get(
    'GTRACKS_GENES_PATH',
    os.path.join(os.path.dirname(__file__), 'genes.bed12.bed.gz')
)
TRACKS = os.environ.get(
    'GTRACKS_TRACKS',
    os.path.join(os.path.dirname(__file__), 'bigWigExample.bw')
).split(',')

COORD_REGEX = re.compile('chr[1-9XY]+:[0-9]+-[0-9]+$')



# Functions ====================================================================

def make_tracks_file(
    *tracks,
    vlines_bed=None,
    genes=None,
    max='auto',
    temp_dir=None,
    color_palette=COLOR_PALETTE,
    genes_height=2,
    gene_rows=1
):
    return (
        '\n'.join(
            BIGWIG_CONFIG_FORMAT.format(
                file=track,
                title=os.path.basename(track).split('.')[0],
                color=color,
                max=max
            )
            for track, color in zip(tracks, color_palette[:len(tracks)])
        )
        + SPACER
        + bool(genes) * GENES_CONFIG_FORMAT.format(genes, genes_height, gene_rows)
        + X_AXIS_CONFIG
        + bool(vlines_bed) * VLINES_CONFIG_FORMAT.format(vlines_bed)
    )


def generate_plot(region, tracks_file, output_file, width: int = 40):
    subprocess.run(
        (
            'pyGenomeTracks',
            '--tracks', tracks_file,
            '--region', region,
            '--outFileName', output_file,
            '--width', str(width)
        )
    )


def parse_region(region):
    chrom, start, end = region.replace('-', ':').split(':')
    return chrom, int(start), int(end)


def parse_gene(gene):
    with gzip.open(GENES_PATH, 'rt') as f:
        for line in f:
            parsed_line = line.split()
            if parsed_line[3] == gene:
                chrom, start, end = parsed_line[:3]
                break
        else:
            raise RuntimeError('gene not found')
    return chrom, int(start), int(end)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Plot BigWig signal tracks and gene annotations in a genomic '
            'region'
        )
    )
    parser.add_argument(
        'region',
        metavar='<{chr:start-end,GENE}>',
        help='coordinates or gene name to plot'
    )
    parser.add_argument(
        'track',
        metavar='<track.bw>',
        nargs='*',
        default=TRACKS,
        help='BigWig files containing tracks'
    )
    parser.add_argument(
        'output',
        metavar='<path/to/output.{pdf,png,svg}>',
        help='path to output file'
    )
    parser.add_argument(
        '--genes',
        metavar='<path/to/genes.bed.gz>',
        default=GENES_PATH,
        help='compressed 6-column BED file containing gene annotations'
    )
    parser.add_argument(
        '--color-palette',
        metavar='<#color>',
        nargs='+',
        default=COLOR_PALETTE,
        help='color pallete for tracks'
    )
    parser.add_argument(
        '--max',
        metavar='<float>',
        type=float,
        help='max value of y-axis'
    )
    parser.add_argument(
        '--tmp-dir',
        metavar='<temp/file/dir>',
        help='directory for temporary files'
    )
    parser.add_argument(
        '--width',
        metavar='<int>',
        type=int,
        default=40,
        help='width of plot in cm'
    )
    parser.add_argument(
        '--genes-height',
        metavar='<int>',
        type=int,
        default=2,
        help='height of genes track'
    )
    parser.add_argument(
        '--gene-rows',
        metavar='<int>',
        type=int,
        default=1,
        help='number of gene rows'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    if not any(args.output.endswith(ext) for ext in ('pdf', 'png', 'svg')):
        raise RuntimeError(
            'Please make sure the output file extension is pdf, png, or svg'
        )
    if COORD_REGEX.match(args.region):
        chrom, xmin, xmax = parse_region(args.region)
    else:
        chrom, start, end = parse_gene(args.region)
        center = (end + start) / 2
        xmin = int(center - 0.55 * (end - start))
        xmax = int(center + 0.55 * (end - start))
    with tempfile.NamedTemporaryFile(dir=args.tmp_dir) as temp_tracks:
        tracks_file = make_tracks_file(
            *args.track,
            genes=args.genes,
            max=args.max,
            color_palette=args.color_palette,
            genes_height=args.genes_height,
            gene_rows=args.gene_rows
        )
        temp_tracks.write(tracks_file.encode())
        temp_tracks.seek(0)
        generate_plot(
            f'{chrom}:{xmin}-{xmax}', temp_tracks.name, args.output,
            width=args.width
        )
