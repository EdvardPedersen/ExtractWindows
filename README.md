# ExtractWindows

## Required files:
input.tsv
----------
A tab-separated file with input data.

windows.tsv
----------
A tab-separated file describing stages and windows in the input data.
Format follows the following formula:
Stage1    Time from start of recording
Window1   Time from start of stage
Window2   Time from start of stage
Stage2    Time from start of recording
Window1   Time from start of stage

## How to use

- Adjust windows in windows.tsv to match your input data
- Export your file from Excel to a tab-separated text file in the same directory as config_parse.exe
- Run config_parse.exe
- Open results.tsv in Excel
