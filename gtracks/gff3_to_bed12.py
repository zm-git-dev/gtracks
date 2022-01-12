#===============================================================================
# gff3_to_bed12.py
#===============================================================================

"""Convert gff3 data to bed12 format"""




# Imports ======================================================================

from argparse import ArgumentParser
from pybedtools import BedTool




# Functions ====================================================================

def parse_gff_attributes(attr):
    return dict(pair.split('=') for pair in attr.split(';'))


def parse_gff(gff: str, type='gene'):
    with open(gff) as f:
        for l in f:
             if not l.startswith('##'):
                seqid, _, t, start, end, _, strand, _, attr = l.rstrip().split(
                                                                           '\t')
                if ((t == type) or (type is None)):
                    yield (seqid, int(start), int(end), strand,
                           parse_gff_attributes(attr))


def generate_bed(gff, type='gene'):
    for seqid, start, end, strand, attr in parse_gff(gff, type=type):
        yield seqid, start, end, attr['ID'], 0, strand


def parse_arguments():
    parser = ArgumentParser(description='convert gff3 to bed12')
    parser.add_argument('gff', metavar='<input.gff3>', help='input gff3 file')
    return parser.parse_args()


def main():
    args = parse_arguments()
    genes = BedTool(tuple(generate_bed(args.gff))).sort()
    exons = BedTool(tuple(generate_bed(args.gff, type='exon'))).sort()
    cds = BedTool(tuple(generate_bed(args.gff, type='CDS'))).sort()
    for gene in genes:
        block_size, block_start = zip(
            *((str(exon.stop - exon.start), str(exon.start - gene.start))
              for exon in exons.intersect(BedTool((gene,)))))
        thick = tuple(cds.intersect(BedTool((gene,))))
        if thick:
            thick_start = thick[0].start
            thick_stop = thick[-1].end
        else:
            thick_start = gene.start
            thick_stop = gene.start
        print('\t'.join(str(x) for x in tuple(gene) + (thick_start, thick_stop,
            '0,0,0', len(block_size), ','.join(block_size)+',',
            ','.join(block_start)+',')))


if __name__ == '__main__':
    main()
