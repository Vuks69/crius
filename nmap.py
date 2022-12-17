#!/usr/bin/env python

import xml.etree.ElementTree as ET
import subprocess
import sys
from handleJson import readJson, writeJson


def nmap(
    target_spec: str,
    mode: str = None,
    interface: str = None,
):
    """
    nmap [Scan Type(s)] [Options] {target specification}
    """
    if target_spec is None:
        print("No target_spec or network provided. Exiting.")
        sys.exit(1)

    command = ["nmap"]
    if mode == "minimal":
        command += ["-nsP"]
    elif mode in ("full", "services"):
        command += ["-sV"]

    if interface is not None:
        command += ["-e", interface]

    command += ["-oX", "nmap_out.xml", target_spec]
    print(" ".join(command))
    subprocess.Popen(command).wait()


def parse_nmap_xml():
    xmlRoot = ET.parse("nmap_out.xml").getroot()

    hosts = readJson()

    for host in xmlRoot.iter("host"):
        addr = host.find("address").attrib["addr"]
        ports = {"ports": {}}
        ssh_port = -1
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
                if port.find("service").attrib["name"] == "ssh":
                    ssh_port = port.attrib["portid"]

        found = False
        for key in hosts:
            if key == "timestamp":
                continue
            jhost: dict = hosts[key]
            if jhost["IP Address"] == addr:
                found = True
                if "ports" in jhost.keys():
                    for portnum in jhost["ports"]:
                        if jhost["ports"][portnum]["product"] not in (None, "null"):
                            ports["ports"][portnum]["product"] = jhost["ports"][portnum]["product"]
                jhost.update(ports)
                if ssh_port != -1:
                    jhost.update({"ssh": ssh_port})
                break
        if not found:
            jhost = {"IP Address": addr}
            if ssh_port != -1:
                jhost.update({"ssh": ssh_port})
            jhost.update(ports)
            hosts.update({len(hosts.keys()) - 1: jhost})

    writeJson(hosts)


if len(sys.argv) == 2:
    nmap(sys.argv[1])
elif len(sys.argv) == 3:
    nmap(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 4:
    nmap(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print(
        """Syntax:
./nmap.py <target_spec range or network> [minimal|full] [interface]
Examples:
    ./nmap.py 10.0.0.0-10
    ./nmap.py 10.0.0.0/24 minimal
    ./nmap.py 10.0.2.0/24 full eth0
    ./nmap.py 10.0.0-2.0-254 minimal eth0"""
    )
    sys.exit(1)

parse_nmap_xml()
