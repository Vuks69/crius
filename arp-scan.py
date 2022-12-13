import subprocess
import json
import sys

arp_scan_args = ["arp-scan", "--localnet"]

if len(sys.argv) > 1:
    arp_scan_args.append("--interface=" + sys.argv[1])

process = subprocess.Popen(arp_scan_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate()
parsed = out.decode().split("\n")[2:-4]

# <IP Address>     <Hardware Address>     <Vendor Details>

i = 0
info_dict = {}
for row in parsed:
    split_row = row.split("\t")
    ip_addr, mac_addr, vendor_details = split_row

    info_dict.update(
        {i:
            {
                "IP Address": ip_addr,
                "Hardware Address": mac_addr,
                "Vendor Details": vendor_details
            }
        }
    )
    i += 1

json_string = json.dumps(info_dict, indent=4)

with open('json_data.json', 'w') as outfile:
    outfile.write(json_string)
