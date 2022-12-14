#!/usr/bin/env python

import subprocess
import sys

from parse_nmap_xml import parse_nmap_xml


def nmap(
    address: str,
    mode: str = None,
    interface: str = None,
):
    if address is None:
        print("No address or network provided. Exiting.")
        sys.exit(1)

    command = ["nmap"]
    if mode == "minimal":
        command += ["-nsP"]
    elif mode == "full" or mode == "services":
        command += ["-sV"]

    if interface is not None:
        command += ["-e", interface]

    command += ["-oX", "nmap_out.xml", address]
    print(" ".join(command))
    subprocess.Popen(command).wait()

    parse_nmap_xml()
