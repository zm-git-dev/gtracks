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

### Example with non-human data and BED track

This example command uses data from _S. polyrhiza_ and includes a BED track.

```sh
gtracks --genes Sp9512 7:6975000-6989000 sp9512_frond_example.bw sp9512_turion_example.bw sp9512_frond_turion_dmr.bed test-non-human.png
```

![test plot non human](https://github.com/anthony-aylward/gtracks/raw/master/test-non-human.png)

## Environment variables

If you want to use your own bigWig files but don't want to write out their
paths every time you run `gtracks`, you can set your own default tracks using
the environment variable `GTRACKS_TRACKS`.
```sh
export GTRACKS_TRACKS=track1.bw,track2.bw,track3.bw
gtracks output.pdf
```

You can also change the default gene annotations file and color palette using
environment variables `GTRACKS_GENES_PATH` and `GTRACKS_COLOR_PALETTE`.
```sh
export GTRACKS_GENES_PATH=path/to/genes.bed.gz
export GTRACKS_COLOR_PALETTE="#color1,#color2,#color3"
gtracks output.pdf
```

Should your genomic coordinates take a different form from the included default
regex, you may set a different default regex using `GTRACKS_COORD_REGEX`:
```sh
export GTRACKS_COORD_REGEX='[\s\S]+:[0-9]+-[0-9]+$'
```

## Usage

```
usage: gtracks [-h] [--genes <{path/to/genes.bed.gz,GRCh37,GRCh38,hg19,hg38,Sp9512}>]
               [--color-palette <#color> [<#color> ...]] [--max <float>] [--tmp-dir <temp/file/dir>] [--width <int>]
               [--genes-height <int>] [--gene-rows <int>] [--x-axis {top,bottom,none}]
               [--vlines-bed <path/to/vlines.bed>] [--bed-labels]
               <{chr:start-end,GENE}> [<track.{bw,bed}> [<track.{bw,bed}> ...]] <path/to/output.{pdf,png,svg}>

Plot bigWig signal tracks and gene annotations in a genomic region

positional arguments:
  <{chr:start-end,GENE}>
                        coordinates or gene name to plot
  <track.{bw,bed}>      bigWig or bed files containing tracks
  <path/to/output.{pdf,png,svg}>
                        path to output file

optional arguments:
  -h, --help            show this help message and exit
  --genes <{path/to/genes.bed.gz,GRCh37,GRCh38,hg19,hg38,Sp9512}>
                        compressed 6-column BED file or 12-column BED12 file containing gene annotations. Alternatively,
                        providing a genome identifier will use one of the included gene tracks. (default: GRCh37)
  --color-palette <#color> [<#color> ...]
                        color pallete for tracks
  --max <float>         max value of y-axis
  --tmp-dir <temp/file/dir>
                        directory for temporary files
  --width <int>         width of plot in cm (default: 40)
  --genes-height <int>  height of genes track (default: 2)
  --gene-rows <int>     number of gene rows (default: 1)
  --x-axis {top,bottom,none}
                        where to draw the x-axis (default: top)
  --vlines-bed <path/to/vlines.bed>
                        BED file defining vertical lines
  --bed-labels          include labels on BED tracks
  --coord-regex <regex>
                        regular expression indicating the format for coordinates (default: ([Cc]hr)?[0-9XY]+:[0-9]+-[0-9]+$)
```
