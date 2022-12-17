import time
import json


def writeJson(data: dict):
    data.update({"timestamp": time.time()})
    json_string = json.dumps(data, indent=4)
    with open("json_data.json", "w") as outfile:
        outfile.write(json_string)
