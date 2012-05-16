#!/usr/bin/python

#
# "begin" command for matching against "show *" output from vtysh.
# When a line gets matched, we will show everything from then onwards.
#

import sys;
import re;

if sys.stdin.isatty():
	sys.stderr.write('ERROR: You must pass some input to this script.\n');
	sys.exit(1);

if len(sys.argv) < 2:
	sys.stderr.write('You need to pass something to match.\n');
	sys.exit(1)

inputLines = sys.stdin.readlines();

lastLine = '';
output = '';

regex = ' '.join(sys.argv[1:]);

if not regex.startswith('^'):
	regex = '^.*' + regex + '.*$'

showlines = False;

for line in inputLines:
	line = line.rstrip();

	if showlines:
		output += line + '\n';
	elif re.match(regex, line):
		output += line + '\n';
		showlines = True;

print output.rstrip();