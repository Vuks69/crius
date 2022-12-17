import time
import json


def readJson():
    with open("json_data.json") as fd:
        hosts = json.load(fd)
    return hosts


def writeJson(data: dict):
    data.update({"timestamp": time.time()})
    json_string = json.dumps(data, indent=4)
    with open("json_data.json", "w") as outfile:
        outfile.write(json_string)
