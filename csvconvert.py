#! /usr/bin/env python

# Command line arguments
import argparse
parser = argparse.ArgumentParser(description="Convert delimited file from one delimiter to another; defaults to converting CSV to pipe-delimited.")
parser.add_argument("--dlm-input", action="store", dest="dlm_in", default=",", required=False, help="delimiter of the input file; defaults to comma (,)", nargs='?', metavar="','")
parser.add_argument("--dlm-output", action="store", dest="dlm_out", default="|", required=False, help="delimiter of the output file; defaults to pipe (|)", nargs='?', metavar="'|'")
parser.add_argument("--remove-line-char", action="store_true", dest="remove_line_char", default=False, help="remove \\n and \\r characters in fields and replace with spaces")
parser.add_argument("--quote-char", action="store", dest="quote_char", default='"', required=False, help="quote character; defaults to double quote (\")", nargs='?', metavar="\"")
parser.add_argument("-i", "--input", action="store", dest="input", required=False, help="input file; defaults to standard input", nargs='?', metavar="file.csv")
parser.add_argument("-o", "--output", action="store", dest="output", required=False, help="output file; defaults standard output", nargs='?', metavar="file.pipe")
parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False, help="increase verbosity")
args  =  parser.parse_args()
# print args

# http://snipplr.com/view/45759/convert-csv-file-to-pipe-delineated-file/
import argparse
import csv
import sys
from signal import signal, SIGPIPE, SIG_DFL # http://stackoverflow.com/questions/14207708/ioerror-errno-32-broken-pipe-python
signal(SIGPIPE,SIG_DFL) ## no error when exiting a pipe like less

if args.input:
    csv_reader = csv.reader(open(args.input, 'rb'), delimiter=args.dlm_in, quotechar=args.quote_char)
else:
    csv_reader = csv.reader(sys.stdin, delimiter=args.dlm_in, quotechar=args.quote_char)

if args.output:
    ofile = open(args.output, 'wb')
else:
    ofile = sys.stdout

for row in csv_reader:
    row = args.dlm_out.join(row)
    if args.remove_line_char:
        row  =  row.replace('\n', ' ').replace('\r', ' ')
    ofile.write("%s\n" % (row))
    ofile.flush()
    # print row
