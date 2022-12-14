#!/usr/bin/env python

import subprocess
import sys
from handleJson import writeJson

arp_scan_args = ["arp-scan", "--localnet"]

if len(sys.argv) > 1:
    arp_scan_args.append("--interface=" + sys.argv[1])

process = subprocess.Popen(
    arp_scan_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
out, err = process.communicate()
parsed = out.decode().split("\n")[2:-4]

# <IP Address>     <Hardware Address>     <Vendor Details>

i = 0
found_hosts = {}
for row in parsed:
    split_row = row.split("\t")
    ip_addr, mac_addr, vendor_details = split_row
    if len(sys.argv) > 1:
        arp_fingerprint = 'arp-fingerprint -o "-N -I ' + sys.argv[1] + '" ' + ip_addr
    else:
        arp_fingerprint = "arp-fingerprint " + ip_addr
    process = subprocess.Popen(
        arp_fingerprint, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    fingerprint, os = out.decode().strip().split("\t")[1:]

    found_hosts.update(
        {
            i: {
                "IP Address": ip_addr,
                "Hardware Address": mac_addr,
                "Vendor Details": vendor_details,
                "Fingerprint": fingerprint,
                "Operating system": os,
            }
        }
    )

    i += 1

writeJson(found_hosts)
