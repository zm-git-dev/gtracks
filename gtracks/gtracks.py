#===============================================================================
# gtracks.py
#===============================================================================

"""Plot ATAC-seq read density and gene annotations around a gene"""




# Imports ======================================================================

import os
import os.path
import subprocess
import seaborn as sns




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
