#===============================================================================
# plot_gene.py
#===============================================================================

"""plot genome track data in a region"""

import argparse
import gzip
import tempfile

from gtracks.gtracks import (
    GENES_PATH, COLOR_PALETTE, TRACKS, make_tracks_file, generate_plot
)


# Functions ====================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Plot ATAC-seq read density and gene annotations in a genomic '
            'region'
        )
    )
    parser.add_argument(
        'region',
        metavar='<chr:start-end>',
        help='coordinates of the region to plot'
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
        metavar='<path/to/output.{pdf,png,svg}',
        help='path to output file'
    )
    parser.add_argument(
        '--genes',
        metavar='<genes.bed.gz>',
        default=GENES_PATH,
        help='compressed 6-column BED file containing gene annotations'
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
    with tempfile.NamedTemporaryFile(dir=args.tmp_dir) as temp_tracks:
        tracks_file = make_tracks_file(
            *args.track,
            genes=args.genes,
            max=args.max,
            color_palette=COLOR_PALETTE,
            genes_height=args.genes_height,
            gene_rows=args.gene_rows
        )
        temp_tracks.write(tracks_file.encode())
        temp_tracks.seek(0)
        generate_plot(
            args.region, temp_tracks.name, args.output, width=args.width
        )
