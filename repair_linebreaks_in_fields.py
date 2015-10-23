#! /usr/bin/env python

# Command line arguments
import argparse
parser = argparse.ArgumentParser(description="Remove line breaks within data fields (so each line has at least the same number of delimiters as line 1).")
parser.add_argument("--dlm", action="store", dest="dlm", default="|", required=False, help="delimiter of the input file; defaults to pipe (|)", nargs='?', metavar="'|'")
parser.add_argument("-i", "--input", action="store", dest="input", required=False, help="input file; defaults to standard input", nargs='?', metavar="input.csv")
parser.add_argument("-o", "--output", action="store", dest="output", required=False, help="output file; defaults standard output", nargs='?', metavar="output.csv")
args  =  parser.parse_args()

# Input and Output files
import sys
from signal import signal, SIGPIPE, SIG_DFL # http://stackoverflow.com/questions/14207708/ioerror-errno-32-broken-pipe-python
signal(SIGPIPE,SIG_DFL) ## no error when exiting a pipe like less

if args.input:
    ifile = open(args.input, 'rb')
else:
    ifile = sys.stdin

if args.output:
    ofile = open(args.output, 'wb')
else:
    ofile = sys.stdout

# Go!
line = ifile.readline()
n_dlm = line.count(dlm)

line0 = line
line_next = 'a'
while line:
    if line.count(dlm) > n_dlm or line_next=='':
        ofile.write(line0)
        line = line_next
        # line = ifile.readline()
        if line.count(dlm) > n_dlm: ## What if a line has more delimiters?  Don't want infinite loop
            line0 = line_next
            line_next = ifile.readline()
            line = line.replace('\r', ' ').replace('\n', ' ') + line_next
    else:
        line0 = line
        line_next = ifile.readline()
        line = line.replace('\r', ' ').replace('\n', ' ') + line_next
