This repo holds Devin Hansen's solution to the Insight Data Engineering challenge.

The goal of this project is to parse a potentially large list of campaign contributions presented in FEC format, and:

1) Identify repeat donors

2) Report the total number and amount of contributions to a campaign from each zip code each year

3) Report on a specified percentile of individual donation for each zip code for a given year


The 'src' folder contains a single program, 'donation-analytics.py', which takes 3 arguments.
The first is the file location of an input data file.  This must be a text file formatted consistantly with FEC guidlines.
The second is the file location of a text file containing a single integer representing the percentile to be reported in the output file.
The third is the file location where the output file will be printed.

'run.sh' will run the app 'donation-analytics.py' on the input files located in the input folder and generate an output file 'repeat_donors.txt' to the output folder.

