#!/bin/python

import json
import sys
import time
from datetime import datetime
from collections import OrderedDict


input_file1 = sys.argv[1]
input_file2 = sys.argv[2]
input_file3 = sys.argv[3]
json_file = sys.argv[4]

if len(sys.argv) != 5:
    print("Usage: python3 convert_to_upb_format.py trn01crd.csv trn01rss.csv trn01tms.csv test.json")
    sys.exit()

# Using readlines()
input_rss = open(input_file2, 'r')
input_crd = open(input_file1, 'r')
input_tms = open(input_file3, 'r')
rss_lines = input_rss.readlines()
crd_lines = input_crd.readlines()
tms_lines = input_tms.readlines()

json_content = {}

c = 0 # collection number
for i in range(0, len(rss_lines), 6):
#     print(crd_lines[i].split(",")[2].rstrip("\n"))
#     print(str(crd_lines[i].split(",")[1]))
    wifi = {}
    for k in range(i, i+6,1):
        for j in range(0, len(rss_lines[k].split(',')), 1):
            if int(rss_lines[k].split(',')[j]) == 100:
                continue
            if "AP"+str(j) in wifi:
                if isinstance(wifi["AP"+str(j)]["rssi"], str):
                    wifi["AP"+str(j)]["rssi"] = [int(rss_lines[k].split(',')[j])]
                if isinstance(wifi["AP"+str(j)]["rssi"], int):
                    wifi["AP"+str(j)]["rssi"] = [rss_lines[k].split(',')[j]]
                if isinstance(wifi["AP"+str(j)]["rssi"], list):
                    a = int(rss_lines[k].split(',')[j])
                    wifi["AP"+str(j)]["rssi"].append(a)
            else:
                wifi["AP"+str(j)] = {"ssid":"?", "frequency":"?", "rssi": [int(rss_lines[k].split(',')[j])]}

    ordWifi = sorted([int(x[2:]) for x in wifi.keys()])
    newWifi = OrderedDict()
    for key in ordWifi:
        newWifi["AP"+str(key)] = wifi["AP"+str(key)]


    fingerprints = []
    x = datetime(int(tms_lines[i][0:4]), int(tms_lines[i][4:6]), int(tms_lines[i][6:8]), \
                 int(tms_lines[i][8:10]), int(tms_lines[i][10:12]), int(tms_lines[i][12:14]))
    fingerprints.append({"timestamp": x.strftime('%d-%m-%Y %H:%M:%S'), "wifi": wifi, "ble": {}, "gps": [], "telephony": []})
    json_content["collection"+str(c)] = {"devId":"?", "devName":"?", "AndroidVersion": "?",\
                                    "comment": "tau", "map":"tau",\
                                    "x":float(crd_lines[i].split(",")[0]),\
                                    "y":float(crd_lines[i].split(",")[1]),\
                                    "z":float(crd_lines[i].split(",")[2].rstrip("\n")),
                                    "fingerprints": fingerprints}
    c += 1

with open(json_file, 'w') as outfile:
    json.dump(json_content, outfile, indent=4)
#     json.dumps({int(x):json_content[x] for x in json_content}, outfile, indent = 4, sort_keys=True)
