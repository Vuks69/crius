#!/usr/bin/env python

import json
from pexpect import pxssh

# Opening JSON file
f = open("json_data.json")

# returns JSON object as
# a dictionary
data = json.load(f)

hosts_with_ssh = {k: v for k, v in data.items() if "ssh" in v.keys()}

for key in hosts_with_ssh:
    host = hosts_with_ssh[key]
    print("Enter login and password for host " + host["IP Address"])
    login = input("login: ")
    password = input("password: ")
    s = pxssh.pxssh()
    if not s.login(host["IP Address"], login, password, port=host["ssh"]):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")
        s.sendline("service --status-all")
        s.prompt()  # match the prompt
        output = s.before.decode().replace(" ", "").split("\n")[1:-1]
        services = {"services": {}}
        for row in output:
            split_row = row.strip().split("]")
            status = split_row[0][1]
            name = split_row[1]
            services["services"].update({name: status})
        host.update(services)
        s.logout()

data = data.update(hosts_with_ssh)
json_string = json.dumps(data, indent=4)
with open("json_data.json", "w") as outfile:
    outfile.write(json_string)
