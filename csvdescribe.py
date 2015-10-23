#! /usr/bin/env python

# Command line arguments
import argparse
parser = argparse.ArgumentParser(description="Describe a delimited file: variable name, variable type, max length.")
parser.add_argument("--dlm", action="store", dest="dlm", default="|", required=False, help="delimiter of the input file; defaults to pipe (|)", nargs='?', metavar="'|'")
parser.add_argument("-i", "--input", action="store", dest="input", required=False, help="input file; if not specified, use standard input", nargs='?', metavar="input.csv")
parser.add_argument("-o", "--output", action="store", dest="output", required=False, help="output file; if not specified, use standard output", nargs='?', metavar="output.csv")
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
import re
floating = re.compile('^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$') ## http://www.regular-expressions.info/floatingpoint.html

line = ifile.readline() ## header
n_dlm = line.count(dlm)
n_fields = n_dlm + 1

rownum = 1
colnames = line.replace('\r', '').replace('\n', '').split(dlm)

## initialize
data_type = ['num'] * n_fields
data_length = [0] * n_fields

for line in ifile.readlines():
    rownum = rownum + 1
    data_fields = line.replace('\r', '').replace('\n', '').split(dlm)
    if n_fields != len(data_fields):
        print "Error: There are %s fields in row %s (expected %s fields)." % (len(data_fields), rownum, (n_dlm+1))
        sys.exit(1)
    for i in range(n_fields):
        if data_type[i] == 'char':
            pass
        elif floating.match(data_fields[i]) == None:
            data_type[i] = 'char'
        data_length[i] = max(data_length[i], len(data_fields[i]))
    
ofile.write('|'.join(['variable','data_type','data_length'])) ## header
ofile.write('\n'.join('%s|%s|%s' % t for t in zip(colnames, data_type, data_length)))
