#!/usr/bin/env python

import xml.etree.ElementTree as ET
import subprocess
import sys
import json


if len(sys.argv) == 2:
    nmap(sys.argv[1])
elif len(sys.argv) == 3:
    nmap(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 4:
    nmap(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print("Syntax:")
    print("nmap.py <address range or network> [minimal|full] [interface]")
    print("Example: crius 10.0.0.0/24 minimal eth0")
    exit(1)

parse_nmap_xml()


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


def parse_nmap_xml():
    tree = ET.parse("nmap_out.xml")
    root = tree.getroot()

    hosts: dict
    with open("json_data.json") as fd:
        hosts = json.load(fd)

    for host in root.iter("host"):
        # status = host.find("status").attrib["state"]
        addr = host.find("address").attrib["addr"]
        ports = {"ports": {}}
        if host.find("ports") is not None:
            for port in host.find("ports").iter("port"):
                ports["ports"].update(
                    {
                        port.attrib["portid"]: {
                            "state": port.find("state").attrib["state"],
                            "service": port.find("service").attrib["name"],
                            "product": port.find("service").attrib.get("product"),
                        }
                    }
                )

        for key in hosts:
            jhost = hosts[key]
            if jhost["IP Address"] == addr:
                jhost.update(ports)
                break

    json_string = json.dumps(hosts, indent=4)

    with open("json_data.json", "w") as outfile:
        outfile.write(json_string)
