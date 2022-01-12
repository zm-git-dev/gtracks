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


def generate_genes_bed(gff):
    for seqid, start, end, strand, attr in parse_gff(gff):
        yield seqid, start, end, attr['ID'], 0, strand


def generate_exons_bed(gff):
    for seqid, start, end, strand, attr in parse_gff(gff, type='exon'):
        yield seqid, start, end, attr['ID'], 0, strand


def parse_arguments():
    parser = ArgumentParser(description='convert gff3 to bed12')
    parser.add_argument('gff', metavar='<input.gff3>', help='input gff3 file')
    return parser.parse_args()


def main():
    args = parse_arguments()
    genes = BedTool(tuple(generate_genes_bed(args.gff)))
    exons = BedTool(tuple(generate_exons_bed(args.gff)))
    for gene in genes:
        block_size, block_start = zip(
            *((str(exon.stop - exon.start), str(exon.start - gene.start))
              for exon in exons.intersect(BedTool((gene,)))))
        print('\t'.join(str(x) for x in tuple(gene) + (gene.start, gene.start,
            '0,0,0', len(block_size), ','.join(block_size)+',',
            ','.join(block_start)+',')))


if __name__ == '__main__':
    main()
