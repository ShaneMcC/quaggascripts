#!/usr/bin/python

#
# "section" command for matching against "show run" output from vtysh.
# When a line gets matched, we will show everything from then onwards
# until we find a new section. (A section begins with any line starting
# without a space or !)
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
	regex = '^([^\s].*' + regex + '|' + regex + ').*$'

showlines = False;

firstLine = '';
foundNewSection = False;

for line in inputLines:
	line = line.rstrip();

	if not line.startswith('!'):
		if not line.startswith(' '):
			foundNewSection = True;
		else:
			foundNewSection = False;

	if showlines:
		if foundNewSection:
			showlines = False;
		else:
			output += line + '\n';
	elif re.match(regex, line):
		output += line + '\n';
		showlines = True;
		firstLine = line;

print output.rstrip();