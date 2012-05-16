#!/usr/bin/python

#
# "include" command for matching against "show *" output from vtysh.
# Currently tested against "show ip bgp sum" output only.
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

lastMatch = False;
for line in inputLines:
	line = line.rstrip();

	if re.match(regex, line):
		if not lastMatch and re.match('^[a-fA-F0-9:.]+$', lastLine):
			output += lastLine + '\n';
		output += line + '\n';
		lastMatch = True;
	else:
		lastMatch = False;

	lastLine = line;

print output.rstrip();