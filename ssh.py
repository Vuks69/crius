#!/usr/bin/env python

from pexpect import pxssh
from handleJson import readJson, writeJson
import json
import sys
from pexpect import pxssh
import pexpect
import time
import subprocess

verbose = False
if len(sys.argv) > 1 and "-v" in sys.argv:
    verbose = True

data = readJson()

hosts_with_ssh = {k: v for k, v in data.items() if "ssh" in v.keys()}
if len(hosts_with_ssh) != 0:
    print("Create ssh_output_files dir")
    subprocess.Popen(
        "mkdir ssh_output_files", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

for key in hosts_with_ssh:
    host = hosts_with_ssh[key]

    print("Enter login and password for host " + host["IP Address"])
    login = input("login: ")
    password = input("password: ")
    sudo_password = input("sudo password: ")

    s = pxssh.pxssh()
    if not s.login(host["IP Address"], login, password, port=host["ssh"]):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")

        print("List services")
        s.sendline("service --status-all")
        s.prompt()
        if verbose: print(s.before.decode())
        output = s.before.decode().replace(" ", "").split("\n")[1:-1]
        services = {"services": {}}
        for row in output:
            split_row = row.strip().split("]")
            status = split_row[0][1]
            name = split_row[1]
            services["services"].update({name: status})
        hosts_with_ssh[key].update(services)

        print("Copy arp-scan to remote host")
        copy_arp_scan = 'scp -P ' + host["ssh"] + ' arp-scan.py ' + login + '@' + host["IP Address"] + ':/home/' + login
        tempChannel = pexpect.spawn(copy_arp_scan)
        tempChannel.expect('assword:')
        tempChannel.sendline(password)
        time.sleep(1)

        print("Look for packages")
        s.sendline("dpkg-query -W -f='${Status}\n' python3 arp-scan")
        s.prompt()
        query_output = s.before.decode().split("\n")
        packages_to_be_removed = []
        if query_output[0].split(" ")[0] == 'install': packages_to_be_removed.append("python")
        if query_output[1].split(" ")[0] == 'install': packages_to_be_removed.append("arp-scan")
        if verbose: print(query_output)

        print("Install packages")
        s.sendline("sudo apt-get update")
        s.prompt()
        output = s.before.decode()
        if verbose: print(output)

        # remove_packages = False
        # output_split = output.split("\n")
        # new_packages_str = "The following NEW packages will be installed"
        # for line in output_split:
        #     print(line)
        #     if new_packages_str in line:
        #         print("jest sukces")
        #         new_packages_index = output_split.index(line) + 1
        #         packages_to_be_removed = output_split[new_packages_index].split("\t")
        #         remove_packages = True


        s.expect(".*assword.*")
        s.sendline(sudo_password)
        s.prompt()
        if verbose: print(s.before.decode())
        # Reading package lists... Done

        s.sendline("sudo apt install python3 arp-scan")
        s.prompt()
        if verbose: print(s.before.decode())

        print("Run arp-scan")
        s.sendline("sudo python3 arp-scan.py")
        s.prompt()
        if verbose: print(s.before.decode())

        print("Remove arp-scan.py")
        s.sendline("sudo rm -rf arp-scan.py json_data.json")
        s.prompt()
        if verbose: print(s.before.decode())

        if len(packages_to_be_removed) > 0:
            packages_str = " ".join(packages_to_be_removed)
            print("Remove packages: " + packages_str)
            s.sendline("sudo apt remove " + packages_str)
            s.prompt()
            if verbose: print(s.before.decode())

        print("Copy output file")
        scp_out_file = 'scp -P ' + host["ssh"] +\
                       ' ' + login + '@' + host["IP Address"] +\
                       ':/home/' + login +\
                       '/json_data.json ./ssh_output_files/' +\
                       host["IP Address"] + "_ssh_out.json"
        print(scp_out_file)
        tempChannel = pexpect.spawn(scp_out_file)
        tempChannel.expect('assword:')
        tempChannel.sendline(password)
        time.sleep(1)

        s.logout()

data = data.update(hosts_with_ssh)
writeJson(data)
