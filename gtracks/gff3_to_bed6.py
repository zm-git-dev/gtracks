#===============================================================================
# gff3_to_bed12.py
#===============================================================================

"""Convert gff3 data to bed6 format"""




# Imports ======================================================================

from argparse import ArgumentParser
from pybedtools import BedTool




# Functions ====================================================================

def parse_gff_attributes(attr):
    return dict(pair.split('=') for pair in attr.split(';'))


def parse_gff(gff: str, type='gene'):
    with open(gff) as f:
        for l in f:
             if not l.startswith('#'):
                seqid, _, t, start, end, _, strand, _, attr = l.rstrip().split(
                                                                           '\t')
                if ((t == type) or (type is None)):
                    yield (seqid, int(start), int(end), strand,
                           parse_gff_attributes(attr))


def generate_bed(gff, type='gene'):
    for seqid, start, end, strand, attr in parse_gff(gff, type=type):
        yield seqid, start, end, attr['ID'], 0, strand


def parse_arguments():
    parser = ArgumentParser(description='convert gff3 to bed6')
    parser.add_argument('gff', metavar='<input.gff3>', help='input gff3 file')
    return parser.parse_args()


def main():
    args = parse_arguments()
    print(BedTool(tuple(generate_bed(args.gff))).sort())


if __name__ == '__main__':
    main()
