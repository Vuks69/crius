import subprocess
import json

oid_ips = "1.3.6.1.2.1.4.22.1.3"
oid_macs = "1.3.6.1.2.1.4.22.1.2"
oid_desc = "1.3.6.1.2.1.1.1.0"
oid_name = "1.3.6.1.2.1.1.5.0"
oid_uptime = "1.3.6.1.2.1.1.3.0"

# load hosts from json
input_file = open('json_data.json')
input_data = json.load(input_file)
hosts = []
next_host_number = 0
for i in input_data:
    hosts.append(input_data[i]['IP Address'])
    next_host_number += 1
input_file.close()

discovered_hosts = {}  # ip: mac
for host in hosts:
    discovered_hosts[host] = ""

discovered_hosts_name = {}  # ip: name
discovered_hosts_desc = {}  # ip: description

# get IPs and MACs
for host in hosts:
    command_ip = "snmpwalk -Oqv -v1 -c public " + host + " " + oid_ips
    command_mac = "snmpwalk -Oqv -v1 -c public " + host + " " + oid_macs
    process_get_ips = subprocess.Popen(command_ip, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_get_macs = subprocess.Popen(command_mac, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_ips, err = process_get_ips.communicate()
    out_macs, err = process_get_macs.communicate()
    discovered_ips = out_ips.decode().split("\n")
    discovered_macs = out_macs.decode().split("\n")
    for i in range(len(discovered_ips)):
        if discovered_ips[i] != "":
            discovered_hosts[discovered_ips[i]] = discovered_macs[i]

# get names and descriptions
for host in discovered_hosts:
    command_name = "snmpget -Oqv -v1 -c public " + host + " " + oid_name
    command_desc = "snmpget -Oqv -v1 -c public " + host + " " + oid_desc
    process_get_name = subprocess.Popen(command_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_get_desc = subprocess.Popen(command_desc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_name, err = process_get_name.communicate()
    out_desc, err = process_get_desc.communicate()
    name = ""
    desc = ""
    name = out_name.decode().rstrip("\n")
    desc = out_desc.decode().rstrip("\n")
    discovered_hosts_name[host] = name
    discovered_hosts_desc[host] = desc

# to json
hosts_dict = {}
host_dict = {}
for ip in discovered_hosts:
    hosts_dict[next_host_number] = {}
    hosts_dict[next_host_number]["IP Address"] = ip
    hosts_dict[next_host_number]["Hardware Address"] = discovered_hosts[ip]
    hosts_dict[next_host_number]["SNMP Name"] = discovered_hosts_name[ip]
    hosts_dict[next_host_number]["SNMP Description"] = discovered_hosts_desc[ip]
    next_host_number += 1

output = json.dumps(hosts_dict, indent=4)
with open('json_data.json', 'a') as outfile:
    outfile.write(output)
