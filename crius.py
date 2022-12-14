#!/usr/bin/env python

import nmap
import sys


if len(sys.argv) == 2:
    nmap.nmap(sys.argv[1])
elif len(sys.argv) == 3:
    nmap.nmap(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 4:
    nmap.nmap(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print("Syntax:")
    print("crius <address range or network> [minimal|full] [interface]")
    print("Example: crius 10.0.0.0/24 minimal eth0")
