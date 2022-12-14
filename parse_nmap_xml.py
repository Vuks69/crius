#!/usr/bin/env python
import xml.etree.ElementTree as ET
import json


def parse_nmap_xml():
    tree = ET.parse("nmap_out.xml")
    root = tree.getroot()

    hosts = []
    for host in root.iter("host"):
        status = host.find("status").attrib["state"]
        addr = host.find("address").attrib["addr"]
        if host.find("ports") is not None:
            ports = [
                {
                    "portid": port.attrib["portid"],
                    "state": port.find("state").attrib["state"],
                    "service": port.find("service").attrib["name"],
                    "product": port.find("service").attrib.get("product"),
                }
                for port in host.find("ports").iter("port")
            ]
        else:
            ports = []

        hosts.append(
            {
                "status": status,
                "address": addr,
                "ports": ports,
            }
        )

    json_string = json.dumps(hosts, indent=4)

    with open("nmap_data.json", "w") as outfile:
        outfile.write(json_string)
