#!/bin/sh

function show() { vtysh -c "show $*" ; }
function i() { /root/peering-scripts/include.py "$@"; }
function inc() { /root/peering-scripts/include.py "$@"; }
function include() { /root/peering-scripts/include.py "$@"; }

function b() { /root/peering-scripts/begin.py "$@"; }
function beg() { /root/peering-scripts/begin.py "$@"; }
function begin() { /root/peering-scripts/begin.py "$@"; }

function s() { /root/peering-scripts/section.py "$@"; }
function sec() { /root/peering-scripts/section.py "$@"; }
function section() { /root/peering-scripts/section.py "$@"; }

function bgpsum() {
  if [ "" = "${1}" ]; then
    show ip bgp sum;
    show ipv6 bgp sum;
  else
    show ip bgp sum | include "$@"
    show ipv6 bgp sum | include "$@"
  fi;
}

function addPeer  { /root/peering-scripts/addPeer.py "$@"; }

