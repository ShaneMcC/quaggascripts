#!/usr/bin/python

#
# Simple python script to make adding peering easier.
#
# Usage: ./addPeer.py <ASNumber> AS-SET <ip1> [ip2] [ip3] .. [ipN]
#
# This will then add the peers directly into quagga.
#

import sys;
import re;
import subprocess;
import os;
from ipcalc import Network, IP;

# Valid Peering IPs:

ourAS = 'XXXXXX';

validPeers = {'LINX-PEER-224': '195.66.224.XXX/23',
              'LINX-PEER-224-V6': '2001:7f8:4::XXXX:1/64',
              'LINX-PEER-226': '195.66.236.XXX/22',
              'LINX-PEER-226-V6': '2001:7f8:4:1::XXXX:1/64',
              'AMSIX-PEER': '195.69.144.XXX/22',
              'AMSIX-PEER-V6': '2001:7f8:1::a5XX:XXXX:1/64',}

peerGroupNames = {'LINX-PEER-224': 'LINX-JUNIPER',
                  'LINX-PEER-224-V6': 'LINX-JUNIPER',
                  'LINX-PEER-226': 'LINX-EXTREME',
                  'LINX-PEER-226-V6': 'LINX-EXTREME',
                  'AMSIX-PEER': 'AMSIX',
                  'AMSIX-PEER-V6': 'AMSIX'}

sys.stderr.write(peerGroupNames);

if len(sys.argv) < 4:
	sys.stderr.write('Usage: ' + sys.argv[0] + ' <ASNumber> AS-SET <ip1> [ip2] [ip3] .. [ipN]\n')
	sys.exit(1)

asnumber = sys.argv[1];
asset = sys.argv[2];

if not re.match("^[0-9]+$", asnumber):
	sys.stderr.write('AS Number: ' + asnumber + ' is not numeric\n')
	sys.exit(1)

if not re.match("^AS([0-9]+|-[A-Z0-9\-]+)$", asset):
	sys.stderr.write('AS SET: ' + asset + ' is not valid. (Must be either AS-SETNAME or AS123456.\n')
	sys.exit(1)

command = 'conf t\n  router bgp ' + ourAS + '\n';

for i in range(3, len(sys.argv)):
	ip = sys.argv[i];
	valid = False;

	for group, range in validPeers.iteritems():
		if ip in Network(range):
			valid = True;
			break;

	if valid:
		command += '    neighbor ' + ip + ' remote-as ' + asnumber + '\n';
		command += '    neighbor ' + ip + ' description Peering via ' + peerGroupNames[group] + ' TO ' + asset + '\n';
		if IP(ip).version() == 4:
			command += '    neighbor ' + ip + ' peer-group ' + group + '\n';
		else:
			command += '    address-family ipv6\n';
			command += '      neighbor ' + ip + ' peer-group ' + group + '\n';
			command += '    exit-address-family\n';

		command += '\n';


command += '  exit\nend\n';

try:
	# Get the right column width...
	env = dict(os.environ);
	rows, columns = os.popen('stty size', 'r').read().split();
	env['COLUMNS'] = columns;

	vtysh = subprocess.Popen(['vtysh'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env);
	stdout, stderr = vtysh.communicate(command);
	print stdout;
except OSError, e:
	print 'Unable to launch quagga, config below: ';
	print command;
