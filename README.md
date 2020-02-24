# gtracks

plot genome track data (for example from bigWig files)

## Installation

```sh
pip3 install gtracks
```
or
```sh
pip3 install --user gtracks
```

## Usage

```
usage: gtracks [-h] [--genes <genes.bed.gz>]
               [--color-palette <#color> [<#color> ...]] [--max <float>]
               [--tmp-dir <temp/file/dir>] [--width <int>]
               [--genes-height <int>] [--gene-rows <int>]
               <{chr:start-end,GENE}> [<track.bw> [<track.bw> ...]]
               <path/to/output.{pdf,png,svg}

Plot bigWig signal tracks and gene annotations in a genomic region

positional arguments:
  <{chr:start-end,GENE}>
                        coordinates or gene name to plot
  <track.bw>            bigWig files containing tracks
  <path/to/output.{pdf,png,svg}>
                        path to output file

optional arguments:
  -h, --help            show this help message and exit
  --genes <genes.bed.gz>
                        compressed 6-column BED file or 12-column BED12 file
                        containing gene annotations
  --color-palette <#color> [<#color> ...]
                        color pallete for tracks
  --max <float>         max value of y-axis
  --tmp-dir <temp/file/dir>
                        directory for temporary files
  --width <int>         width of plot in cm
  --genes-height <int>  height of genes track
  --gene-rows <int>     number of gene rows
```

## Examples

```sh
gtracks chr21:33031597-33041570 track1.bw track2.bw output.pdf
gtracks SOD1 track1.bw track2.bw output.png

export GTRACKS_TRACKS=track1.bw,track2.bw
gtracks SOD1 output.svg
```
