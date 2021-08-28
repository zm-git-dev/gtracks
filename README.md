# gtracks

Plot genome track data from bigWig files. Powered by [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks).

## Installation

```sh
pip install gtracks
```
or
```sh
pip install --user gtracks
```

## Examples

An example bigwig file with ATAC-seq data from the insulin region is included.
You can generate a test plot like this:
```sh
gtracks INS-IGF2 test.png
```
![test plot](https://github.com/anthony-aylward/gtracks/raw/master/test.png)

You can plot your own tracks over other genomic regions by providing more
positional arguments: a region or gene name and paths to one or more bigWig
files. The file type of the plot will be determined by the
output file extension.
```sh
gtracks chr11:2150341-2182439 track1.bw track2.bw output.pdf
gtracks INS track1.bw track2.bw output.svg
```

### Modifying the gene annotations track

GRCh37/hg19 gene annotations are used by default, but you can plot GRCh38/hg38
genes by adding `--genes GRCh38` or `--genes hg38`. You can use your own gene
annotations file (BED or BED12 format) by providing
`--genes <path/to/genes.bed.gz>`.

You may want to add more rows to the genes track. You can do this using
the `--genes-height` and `--gene-rows` options.

```sh
gtracks INS test-genes.png --genes-height 6 --gene-rows 6
```
![test plot with more gene rows](https://github.com/anthony-aylward/gtracks/raw/master/test-genes.png)

### Changing the color palette

You can change the color palette for bigWig tracks using the `--color-palette` option.
```sh
gtracks INS track1.bw track2.bw track3.bw output.pdf --color-palette "#color1" "#color2" "#color3"
```

### Setting y-axis height

By default, tracks have different y-axis heights depending on signal height.
You can set a uniform y-axis height for all tracks using the `--max` option.

```sh
gtracks INS track1.bw track2.bw track3.bw output.pdf --max 400
```

For more command-line options, see the usage page below.

## Environment variables

If you want to use your own bigWig files but don't want to write out their
paths every time you run `gtracks`, you can set your own default tracks using
the environment variable `GTRACKS_TRACKS`.
```
export GTRACKS_TRACKS=track1.bw,track2.bw,track3.bw
gtracks output.pdf
```

You can also change the default gene annotations file and color palette using
environment variables `GTRACKS_GENES_PATH` and `GTRACKS_COLOR_PALETTE`.
```
export GTRACKS_GENES_PATH=path/to/genes.bed.gz
export GTRACKS_COLOR_PALETTE="#color1,#color2,#color3"
gtracks output.pdf
```

## Usage

```
usage: gtracks [-h] [--genes <{path/to/genes.bed.gz,GRCh37,GRCh38,hg19,hg38}>]
               [--color-palette <#color> [<#color> ...]] [--max <float>]
               [--tmp-dir <temp/file/dir>] [--width <int>]
               [--genes-height <int>] [--gene-rows <int>]
               <{chr:start-end,GENE}> [<track.bw> [<track.bw> ...]]
               <path/to/output.{pdf,png,svg}>

Plot bigWig signal tracks and gene annotations in a genomic region

positional arguments:
  <{chr:start-end,GENE}>
                        coordinates or gene name to plot
  <track.bw>            bigWig files containing tracks
  <path/to/output.{pdf,png,svg}>
                        path to output file

optional arguments:
  -h, --help            show this help message and exit
  --genes <{path/to/genes.bed.gz,GRCh37,GRCh38,hg19,hg38}>
                        compressed 6-column BED file or 12-column BED12 file
                        containing gene annotations. Alternatively, providing
                        a genome identifier will use one of the included gene
                        tracks. (default: GRCh37)
  --color-palette <#color> [<#color> ...]
                        color pallete for tracks
  --max <float>         max value of y-axis
  --tmp-dir <temp/file/dir>
                        directory for temporary files
  --width <int>         width of plot in cm (default: 40)
  --genes-height <int>  height of genes track (default: 2)
  --gene-rows <int>     number of gene rows (default: 1)
```
