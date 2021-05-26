#!/bin/python

import json
import sys

input_file1 = sys.argv[1]
input_file2 = sys.argv[2]
json_file = sys.argv[3]

if len(sys.argv) != 4:
    print("Usage: python3 convert_to_upb_format.py rm_rss.csv rm_crd.csv test.json")
    sys.exit()

# Using readlines()
input_rss = open(input_file1, 'r')
input_crd = open(input_file2, 'r')
rss_lines = input_rss.readlines()
crd_lines = input_crd.readlines()

json_content = {}

i = 0 # collection number
for i in range(0, len(rss_lines), 1):
#     print(crd_lines[i].split(",")[2].rstrip("\n"))
#     print(str(crd_lines[i].split(",")[1]))
    wifi = {}
    for j in range(0, len(rss_lines[i].split(',')), 1):
        if int(rss_lines[i].split(',')[j]) == 100:
            continue
        wifi["AP"+str(j)] ={"ssid":"?", "frequency":"?", "rssi": [int(rss_lines[i].split(',')[j])]}

    fingerprints = []
    fingerprints.append({"timestamp": "?", "wifi": wifi, "ble": {}, "gps": [], "telephony": []})
    json_content["collection"+str(i)] = {"devId":"?", "devName":"?", "AndroidVersion": "?",\
                                    "comment": "tau", "map":"tau",\
                                    "x":float(crd_lines[i].split(",")[0]),\
                                    "y":float(crd_lines[i].split(",")[1]),\
                                    "z":float(crd_lines[i].split(",")[2].rstrip("\n")),
                                    "fingerprints": fingerprints}


with open(json_file, 'w') as outfile:
    json.dump(json_content, outfile, indent=4)
